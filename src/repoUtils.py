import os
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


def createInfoFile(user_id, repo_name, repo_id, description, url, create_time, visibility):
    content = f'''repository_id,{repo_id}
repository_name,{repo_name}
user_id,{user_id}
url,{url}
description,{description}
create_time,{str(create_time)},
visibility,{visibility}'''

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
    fsUtils.upload_folder(local_path, dropbox_path)
    return True
