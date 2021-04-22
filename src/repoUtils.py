import os
import difflib
from glob import glob
from datetime import date, datetime

from sqlalchemy.sql.expression import desc
from dbUtils import *
import cliUtils
import fsUtils

repoDB = repoDBUtils()
fileDB = fileDBUtils()
commitDB = commitDBUtils()
relationDB = relationDBUtils()
userDB = userDBUtils()



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
    all_repos = repoDB.getAllRepositoryID()
    if not all_repos:
        repo_id = "REPO000001"
    else:
        roll_numbers = sorted([int(i[0][6:]) for i in all_repos])
        new_roll_number = str(roll_numbers[-1] + 1)
        repo_id = f"REPO{new_roll_number.zfill(6)}"
    return repo_id


def generateFileID():
    all_files = fileDB.getAllFileID()
    if not all_files:
        file_id = "FILE000001"
    else:
        roll_numbers = sorted([int(i[0][6:]) for i in all_files])
        new_roll_number = str(roll_numbers[-1] + 1)
        file_id = f"FILE{new_roll_number.zfill(6)}"
    return file_id


def generateCommitID():
    all_commits = commitDB.getAllCommitID()
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

def getRepoOwner(repo_id):
    relations = relationDB.getAllRelations(repo_id)
    owner = ''
    for relation in relations:
        if relation[-1] == "owner":
            owner_id = relation[0]
            break
    owner_name = userDB.getUsername(owner_id)
    return owner, owner_name


def init(cache, repo_name):
    user_id = cache["current_user_id"]
    username = cache["current_username"]
    if repoDB.checkUserRepositoryExists(user_id, repo_name):
        print("Repository names have to be unique per user.")
        return False
    if len(repo_name) > 50:
        print("Repository Name cannot be over 50 chars long")
        return False
    cliUtils.mkdir(repo_name)
    cliUtils.mkdir(os.path.join(repo_name, ".togepi"))
    repo_id = generateRepositoryID()
    description = input("Enter repository description? [y/n]: ")
    if description.lower() == 'n':
        description = None
    else:
        description = input("Enter repository description (under 150 chars): ")
        if len(description) > 150:
            print("Description must be under 150 chars. Truncating description..")
            description = description[:150]
    url = f"/{username}/{repo_name}"
    create_time = datetime.utcnow()
    visibility = input("Enter repository visibility [public/private]: ")

    if visibility not in ["public", "private"]:
        print("Invalid option. Resetting to public.")
        visibility = "public"

    createInfoFile(user_id, repo_name, repo_id, description,
                   url, create_time, visibility)
    repoDB.createRepository(user_id, repo_name, repo_id,
                             description, url, create_time, visibility)
    relationDB.createUserRepositoryRelation(user_id, repo_id)

    dropbox_path = f"/{username}/{repo_name}/"
    # before uploading track the info file
    local_path = os.path.join(os.getcwd(), repo_name)
    fsUtils.uploadFolder(local_path, dropbox_path)
    return True


def initGUI(cache, repo_name, description=None, visibility="public"):
    user_id = cache["current_user_id"]
    username = cache["current_username"]
    if repoDB.checkUserRepositoryExists(user_id, repo_name):
        print("Repository names have to be unique per user.")
        return False, 1
    if len(repo_name) > 50:
        print("Repository Name cannot be over 50 chars long")
        return False, 2
    cliUtils.mkdir(repo_name)
    return_path = os.path.join(os.getcwd(), repo_name)
    cliUtils.mkdir(os.path.join(repo_name, ".togepi"))
    repo_id = generateRepositoryID()
    #     description = input("Enter repository description (under 150 chars): ")
    #     if len(description) > 150:
    #         print("Description must be under 150 chars. Truncating description..")
    #         description = description[:150]
    url = f"/{username}/{repo_name}"
    create_time = datetime.utcnow()
    # if visibility not in ["public", "private"]:
    #     print("Invalid option. Resetting to public.")
    #     visibility = "public"

    createInfoFile(user_id, repo_name, repo_id, description,
                   url, create_time, visibility)
    repoDB.createRepository(user_id, repo_name, repo_id,
                             description, url, create_time, visibility)
    relationDB.createUserRepositoryRelation(user_id, repo_id)

    dropbox_path = f"/{username}/{repo_name}/"
    # before uploading track the info file
    local_path = os.path.join(os.getcwd(), repo_name)
    fsUtils.uploadFolder(local_path, dropbox_path)
    return True, (repo_id, repo_name, user_id, username), return_path


def add(cache, filepaths):

    # check if user_id is collaborator/owner
    # check if files were deleted -- untrack these files by deleting from db (and dropbox folder)
    user_id = cache["current_user_id"]
    repo_id = cache["current_repository_id"]
    relations = relationDB.getAllRelations(repo_id)
    found_user = False
    for relation in relations:
        if relation[0]==user_id:
            repo_relation = relation[-1]
            found_user = True
            break
    if not found_user:
        print("You do not have access to this repository. Cannot add files")
        return False, []
    if filepaths == ".":
        filepaths = [os.path.join(parent, name) for (
            parent, subdirs, files) in os.walk(".") for name in files + subdirs]
    print(filepaths)
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
        if not fileDB.checkFileInDatabase(repo_id, f):
            new_tracked_files.append(f)
    outputs = []
    current_time = datetime.utcnow()
    for tracked_file in new_tracked_files:
        file_id = generateFileID()
        fileDB.createFile(file_id, tracked_file, repo_id,
                           "unchanged", current_time, None, None)
        outputs.append(f"File {tracked_file} successfully tracked.")
    return True, outputs

def commit(cache, message=None):
    user_id = cache["current_user_id"]
    username = cache["current_username"]
    repo_id = cache["current_repository_id"]
    repo_name = cache["current_repository_name"]

    owner_id, owner_name = getRepoOwner(repo_id)
    relations = relationDB.getAllRelations(repo_id)
    found_user = False
    for relation in relations:
        if relation[0]==user_id:
            repo_relation = relation[-1]
            found_user = True
            break
    if not found_user:
        print("You do not have commit access to this repository.")
        return False, ""
    tracked_files = fileDB.getTrackedFiles(repo_id)
    modified_files = dict()

    num_files_changed = 0
    num_diffs = {"add": 0, "del": 0}

    for fname in tracked_files:
        with open(fname) as f:
            local_content = f.read()
        cloud_file_path = f"/{owner_name}/{repo_name}/{fname[2:]}"
        cloud_content = fsUtils.getContent(cloud_file_path)
        diff = getDiff(cloud_content, local_content)
        check, adds, dels = checkFileIsModified(diff)
        if check:
            modified_files[fname] = diff
            last_modified_time = datetime.utcfromtimestamp(
                os.path.getmtime(fname))
            fileDB.updateFileModifiedTime(repo_id, fname, last_modified_time)

            num_files_changed += 1
            num_diffs["add"] += adds
            num_diffs["del"] += dels

    commit_id = generateCommitID()
    current_time = datetime.utcnow()
    current_time_string = "-".join(str(datetime.utcnow())[:19].split())
    folder_name = f".togepi/{commit_id}--{current_time_string}"
    output_str = ''
    for modified_file in modified_files:
        file_id = fileDB.getFileID(repo_id, modified_file)
        if not os.path.exists(folder_name):
            cliUtils.mkdir(folder_name)
        with open(f"{folder_name}/{file_id}.txt", "w") as f:
            f.write(f"{modified_file}\n\n")
            f.write(modified_files[modified_file])
        commitDB.createCommit(commit_id, user_id, repo_id,
                             current_time, file_id, message)
        fileDB.updateFileCommitTime(repo_id, modified_file, current_time)
        print(f"added changes: {modified_file}")
        output_str += f"added changes: {modified_file}\n"
    adds = num_diffs["add"]
    dels = num_diffs["del"]
    print(f"{num_files_changed} files changed: {adds} additions(+) {dels} deletions(-)")
    output_str += f"{num_files_changed} files changed: {adds} additions(+) {dels} deletions(-)\n"
    return True, output_str


def push(cache):
    repo_id = cache["current_repository_id"]
    username = cache["current_username"]
    repo_name = cache["current_repository_name"]
    user_id = cache["current_user_id"]
    relations = relationDB.getAllRelations(repo_id)
    found_user = False
    for relation in relations:
        if relation[0]==user_id:
            repo_relation = relation[-1]
            found_user = True
            break
    if not found_user:
        print("You do not have push access to this repository.")
        return False, []
    owner_id, owner_name = getRepoOwner(repo_id)
    current_time = datetime.utcnow()
    tracked_files = fileDB.getTrackedFiles(repo_id)
    for fname in tracked_files:
        fileDB.updateFilePushTime(repo_id, fname, current_time)

    local_path = f"../{repo_name}"
    dropbox_path = f"/{owner_name}/{repo_name}/"
    output = fsUtils.uploadFolder(local_path, dropbox_path)
    return True, output


def pull(cache):
    repo_id = cache["current_repository_id"]
    username = cache["current_username"]
    repo_name = cache["current_repository_name"]
    user_id = cache["current_user_id"]
    print("inside pull, cache:", cache)
    relations = relationDB.getAllRelations(repo_id)
    found_user = False
    for relation in relations:
        if relation[0]==user_id:
            repo_relation = relation[-1]
            found_user = True
            break
    if not found_user:
        print("You do not have pull access on this repository.")
        return False, 1
    owner_id, owner_name = getRepoOwner(repo_id)
    print(f"cloud path: /{owner_name}/{repo_name}/.togepi")
    most_recent_cloud_commit_time = fsUtils.getRecentCloudCommitTime(
        f"/{owner_name}/{repo_name}/.togepi")
    most_recent_local_commit_time = fsUtils.getRecentLocalCommitTime()

    if most_recent_cloud_commit_time is None:   # check other way round
        print("No commits have been pushed to repository.")
        return False, 2
    elif most_recent_local_commit_time is None:  # check other way round
        print("No commits have been created.")
        return False, 3
    else:
        if most_recent_cloud_commit_time == most_recent_local_commit_time:
            print("No changes to pull, repository is upto date.")
            return False, 4
        else:
            print("Pulling changes...")
            fsUtils.downloadFolder(username, repo_name)
            return True, 0


def status(cache):
    username = cache["current_username"]
    repo_id = cache["current_repository_id"]
    repo_name = cache["current_repository_name"]
    user_id = cache["current_user_id"]
    owner_id, owner_name = getRepoOwner(repo_id)
    tracked_files = fileDB.getTrackedFiles(repo_id)
    relations = relationDB.getAllRelations(repo_id)
    found_user = False
    for relation in relations:
        if relation[0]==user_id:
            repo_relation = relation[-1]
            found_user = True
            break
    if not found_user:
        print("You do not have access on this repository. Cannot see status")
        return
    for fname in tracked_files:
        with open(fname) as f:  # if new file is added but not in local -> error
            local_content = f.read()
        cloud_file_path = f"/{owner_name}/{repo_name}/{fname[2:]}"
        cloud_content = fsUtils.getContent(cloud_file_path)
        diff = getDiff(cloud_content, local_content)
        if checkFileIsModified(diff):
            last_modified_time = datetime.utcfromtimestamp(
                os.path.getmtime(fname))
            fileDB.updateFileModifiedTime(repo_id, fname, last_modified_time)
            print(f"modified: {fname}")

    # display if commits are yet to be pushed
    # display if files in repo aren't being tracked
    # display files deleted from local, but present on cloud


def clone(cache, clone_path):
    repo_username, repo_name = clone_path.split("/")
    repo_id, repo_status = repoDB.getRepoStatus(repo_username, repo_name)
    if repo_status != "public":
        user_id = cache["current_user_id"]
        #print("Trying to clone", repo_id, user_id)
        relations = relationDB.getAllRelations(repo_id)
        found_user = False
        for relation in relations:
            if relation[0]==user_id:
                repo_relation = relation[-1]
                found_user = True
                break
        if not found_user:
            print(f"You are not a collaborator on {repo_name}. Cannot clone private repository")
            return False
        else:
            print(f"Cloning repository {repo_name}...")
            fsUtils.downloadFolder(repo_username, repo_name, pull=False)
            return True
    else:
        print(f"Cloning repository {repo_name}...")
        fsUtils.downloadFolder(repo_username, repo_name, pull=False)
        return True

def addCollaborator(cache, collab_username):
    repo_id = cache["current_repository_id"]
    user_id = cache["current_user_id"]
    print("add collab:", cache)
    relations = relationDB.getAllRelations(repo_id)
    found_user = False
    for relation in relations:
        if relation[0]==user_id and relation[-1]=="owner":
            repo_relation = "owner"
            found_user = True
            break
    if not found_user:
        print("You are not owner of this repository. Cannot add collaborator")
        return False, 1
    collab_user_id = userDB.getUserID(collab_username)
    for relation in relations:
        if relation[0]== collab_user_id:
            return False, 2 #user to be added is already a collaborator
    if collab_user_id == '':
        print(
            f"User {collab_username} does not exist. Please check the username")
        return False, 3
    relationDB.createUserRepositoryRelation(collab_user_id, repo_id, "collaborator")
    print(f"User {collab_username} successfully added as collaborator.")
    return True, 0


