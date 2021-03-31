import os
from glob import glob
from datetime import date, datetime

from sqlalchemy.sql.expression import desc
import dbUtils
import cliUtils
import fsUtils


def generateRepositoryID():
    all_repos = dbUtils.getAllRepositoryID()
    if not all_repos:
        repo_id = "REPO#000001"
    else:
        roll_numbers = sorted([int(i[0][5:]) for i in all_repos])
        new_roll_number = str(roll_numbers[-1] + 1)
        repo_id = f"REPO#{new_roll_number.zfill(6)}"
    return repo_id


def generateFileID():
    all_files = dbUtils.getAllFileID()
    if not all_files:
        file_id = "FILE#000001"
    else:
        roll_numbers = sorted([int(i[0][5:]) for i in all_files])
        new_roll_number = str(roll_numbers[-1] + 1)
        file_id = f"FILE#{new_roll_number.zfill(6)}"
    return file_id


def createInfoFile(user_id, repo_name, repo_id, description, url, create_time, visibility):
    content = f'''repository_id,{repo_id}
repository_name,{repo_name}
user_id,{user_id}
url,{url}
description,{description}
create_time,{str(create_time)},
visibility,{visibility}
collaborators,'''

    with open(f"{repo_name}/.togepi/info.txt", "w") as f:
        f.write(content)


def init(user_id, repo_name):
    if dbUtils.checkUserRepositoryExists(user_id, repo_name):
        print("Repository names have to be unique per user.")
        return False

    cliUtils.mkdir(repo_name)
    cliUtils.mkdir(os.path.join(repo_name, ".togepi"))
    username = dbUtils.getUsername(user_id)
    repo_id = generateRepositoryID()
    description = input("Enter repository description? [y/n]: ")
    if description.lower() == 'n':
        description = None
    else:
        description = input("Enter repository description: ")
    url = f"https://togepi.com/{username}/{repo_name}"
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
    local_path = os.path.join(os.getcwd(), repo_name)
    fsUtils.uploadFolder(local_path, dropbox_path)
    return True


def add(user_id, repo_name, filepaths):

    # check if user_id is collaborator/owner
    # check if files were deleted -- untrack these files by deleting from db (and dropbox folder)

    if filepaths == ".":
        filepaths = [y for x in os.walk(".")
                     for y in glob(os.path.join(x[0], '*.*'))]

    with open(f".togepi/info.txt") as f:
        content = f.read().strip().split('\n')
        _, repo_id = content[0].split(',')
        repo_id = repo_id.strip()

    if ".tgpignore" in os.listdir():
        with open(".tgpignore") as f:
            ignored_files = f.read().strip().split('\n')    # handle dir

    new_tracked_files = list()
    for f in filepaths:
        if not dbUtils.checkFileInDatabase(repo_id, f):  # and check .tgpignore
            new_tracked_files.append(f)

    for tracked_file in new_tracked_files:
        file_id = generateFileID()
        dbUtils.createFile(file_id, tracked_file, repo_id, "unchanged", None, None, None)
