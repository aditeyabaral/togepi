import os
import difflib
from glob import glob
from datetime import date, datetime

from sqlalchemy.sql.expression import desc
import dbUtils
import cliUtils
import fsUtils


def getRepoIdFromDirectory():
    with open(f".togepi/tgpinfo.txt") as f:
        content = f.read().strip().split('\n')
        _, repo_id = content[0].split(',')
        repo_id = repo_id.strip()
    return repo_id


def getDiff(cloud_file_content, local_file_content):
    local_file_content_lines = local_file_content.split('\n')
    cloud_file_content_lines = cloud_file_content.split('\n')
    d = difflib.Differ()
    diff = d.compare(cloud_file_content_lines, local_file_content_lines)
    diff = '\n'.join(diff)
    return diff


def checkFileIsModified(diff):
    lines = diff.split('\n')
    adds = 0
    dels = 0
    for l in lines:
        if l.startswith('+ ') or l.startswith('- ') or l.startswith('? '):
            if l.startswith('+ '):
                adds += 1
            elif l.startswith('- '):
                dels += 1
            else:
                pass
    if adds > 0 or dels > 0:
        return True, adds, dels
    return False, 0, 0


def generateRepositoryID():
    all_repos = dbUtils.getAllRepositoryID()
    if not all_repos:
        repo_id = "REPO000001"
    else:
        roll_numbers = sorted([int(i[0][6:]) for i in all_repos])
        new_roll_number = str(roll_numbers[-1] + 1)
        repo_id = f"REPO{new_roll_number.zfill(6)}"
    return repo_id


def generateFileID():
    all_files = dbUtils.getAllFileID()
    if not all_files:
        file_id = "FILE000001"
    else:
        roll_numbers = sorted([int(i[0][6:]) for i in all_files])
        new_roll_number = str(roll_numbers[-1] + 1)
        file_id = f"FILE{new_roll_number.zfill(6)}"
    return file_id


def generateCommitID():
    all_commits = dbUtils.getAllCommitID()
    if not all_commits:
        commit_id = "COMMIT000001"
    else:
        roll_numbers = sorted([int(i[0][6:]) for i in all_commits])
        new_roll_number = str(roll_numbers[-1] + 1)
        commit_id = f"COMMIT{new_roll_number.zfill(6)}"
    return commit_id


def createInfoFile(user_id, repo_name, repo_id, description, url, create_time, visibility):
    content = f'''repository_id,{repo_id}
repository_name,{repo_name}
user_id,{user_id}
url,{url}
description,{description}
create_time,{str(create_time)},
visibility,{visibility}
collaborators,'''

    with open(f"{repo_name}/.togepi/tgpinfo.txt", "w") as f:
        f.write(content)


def init(cache, repo_name):
    user_id = cache["current_user_id"]
    username = cache["current_username"]
    if dbUtils.checkUserRepositoryExists(user_id, repo_name):
        print("Repository names have to be unique per user.")
        return False

    cliUtils.mkdir(repo_name)
    cliUtils.mkdir(os.path.join(repo_name, ".togepi"))
    repo_id = generateRepositoryID()
    description = input("Enter repository description? [y/n]: ")
    if description.lower() == 'n':
        description = None
    else:
        description = input("Enter repository description: ")
    url = f"/{username}/{repo_name}"
    create_time = datetime.utcnow()
    visibility = input("Enter repository visibility [public/private]: ")

    if visibility not in ["public", "private"]:
        print("Invalid option. Resetting to public.")
        visibility = "public"

    createInfoFile(user_id, repo_name, repo_id, description,
                   url, create_time, visibility)
    dbUtils.createRepository(user_id, repo_name, repo_id,
                             description, url, create_time, visibility)
    dbUtils.createUserRepositoryRelation(user_id, repo_id)

    dropbox_path = f"/{username}/{repo_name}/"
    # before uploading track the info file
    local_path = os.path.join(os.getcwd(), repo_name)
    fsUtils.uploadFolder(local_path, dropbox_path)
    return True


def add(cache, filepaths):

    # check if user_id is collaborator/owner
    # check if files were deleted -- untrack these files by deleting from db (and dropbox folder)

    repo_id = cache["current_repository_id"]

    if filepaths == ".":
        filepaths = [os.path.join(parent, name) for (
            parent, subdirs, files) in os.walk(".") for name in files + subdirs]

    # filepaths = [fname for fname in filepaths if os.path.isfile(fname)]

    ignored_files = list()
    if ".tgpignore" in os.listdir():
        with open(".tgpignore") as f:
            ignored_files = f.read().strip().split('\n')
        temp = list()
        for ig_file in ignored_files:
            if not os.path.isfile(ig_file):
                sub_files = [os.path.join(parent, name) for (
                    parent, subdirs, files) in os.walk(ig_file) for name in files + subdirs]
                temp.extend(sub_files)
            else:
                temp.append(ig_file)
        ignored_files = list(temp)

    filepaths = [fname for fname in filepaths if os.path.isfile(
        fname) and fname not in ignored_files and not fname.startswith("./.togepi/COMMIT")]

    new_tracked_files = list()
    for f in filepaths:
        if not dbUtils.checkFileInDatabase(repo_id, f):
            new_tracked_files.append(f)

    current_time = datetime.utcnow()
    for tracked_file in new_tracked_files:
        file_id = generateFileID()
        dbUtils.createFile(file_id, tracked_file, repo_id,
                           "unchanged", current_time, None, None)


def commit(cache, message=None):
    user_id = cache["current_user_id"]
    username = cache["current_username"]
    repo_id = cache["current_repository_id"]
    repo_name = cache["current_repository_name"]

    tracked_files = dbUtils.getTrackedFiles(repo_id)
    modified_files = dict()

    num_files_changed = 0
    num_diffs = {"add": 0, "del": 0}

    for fname in tracked_files:
        with open(fname) as f:
            local_content = f.read()
        cloud_file_path = f"/{username}/{repo_name}/{fname[2:]}"
        cloud_content = fsUtils.getContent(cloud_file_path)
        diff = getDiff(cloud_content, local_content)
        check, adds, dels = checkFileIsModified(diff)
        if check:
            modified_files[fname] = diff
            last_modified_time = datetime.utcfromtimestamp(
                os.path.getmtime(fname))
            dbUtils.updateFileModifiedTime(repo_id, fname, last_modified_time)

            num_files_changed += 1
            num_diffs["add"] += adds
            num_diffs["del"] += dels

    commit_id = generateCommitID()
    current_time = datetime.utcnow()
    current_time_string = "-".join(str(datetime.utcnow())[:19].split())
    folder_name = f".togepi/{commit_id}--{current_time_string}"
    for modified_file in modified_files:
        file_id = dbUtils.getFileID(repo_id, modified_file)
        if not os.path.exists(folder_name):
            cliUtils.mkdir(folder_name)
        with open(f"{folder_name}/{file_id}.txt", "w") as f:
            f.write(f"{modified_file}\n\n")
            f.write(modified_files[modified_file])
        dbUtils.createCommit(commit_id, user_id, repo_id,
                             current_time, file_id, message)
        dbUtils.updateFileCommitTime(repo_id, modified_file, current_time)
        print(f"added changes: {modified_file}")

    adds = num_diffs["add"]
    dels = num_diffs["del"]
    print(f"{num_files_changed} files changed: {adds} addtions(+) {dels} deletions(-)")


def push(cache):
    repo_id = cache["current_repository_id"]
    username = cache["current_username"]
    repo_name = cache["current_repository_name"]

    current_time = datetime.utcnow()
    tracked_files = dbUtils.getTrackedFiles(repo_id)
    for fname in tracked_files:
        dbUtils.updateFilePushTime(repo_id, fname, current_time)

    local_path = f"../{repo_name}"
    dropbox_path = f"/{username}/{repo_name}/"
    fsUtils.uploadFolder(local_path, dropbox_path)


def pull(cache):
    repo_id = cache["current_repository_id"]
    username = cache["current_username"]
    repo_name = cache["current_repository_name"]

    most_recent_cloud_commit_time = fsUtils.getRecentCloudCommitTime(
        f"/{username}/{repo_name}/.togepi")
    most_recent_local_commit_time = fsUtils.getRecentLocalCommitTime()

    if most_recent_cloud_commit_time is None:   # check other way round
        print("No commits have been pushed to repository.")
    elif most_recent_local_commit_time is None:  # check other way round
        print("No commits have been created.")
    else:
        if most_recent_cloud_commit_time == most_recent_local_commit_time:
            print("No changes to pull, repository is upto date.")
        else:
            print("Pulling changes...")
            fsUtils.downloadFolder(username, repo_name)


def status(cache):
    username = cache["current_username"]
    repo_id = cache["current_repository_id"]
    repo_name = cache["current_repository_name"]

    tracked_files = dbUtils.getTrackedFiles(repo_id)

    for fname in tracked_files:
        with open(fname) as f:  # if new file is added but not in local -> error
            local_content = f.read()
        cloud_file_path = f"/{username}/{repo_name}/{fname[2:]}"
        cloud_content = fsUtils.getContent(cloud_file_path)
        diff = getDiff(cloud_content, local_content)
        if checkFileIsModified(diff):
            last_modified_time = datetime.utcfromtimestamp(
                os.path.getmtime(fname))
            dbUtils.updateFileModifiedTime(repo_id, fname, last_modified_time)
            print(f"modified: {fname}")

    # display if commits are yet to be pushed
    # display if files in repo aren't being tracked
    # display files deleted from local, but present on cloud


def clone(cache, clone_path):
    repo_username, repo_name = clone_path.split("/")
    repo_status = dbUtils.getRepoStatus(repo_username, repo_name)
    if repo_status != "public":
        print("Repository is public. Not available for cloning")
        return
    print(f"Cloning repository {repo_name}...")
    fsUtils.downloadFolder(repo_username, repo_name)
