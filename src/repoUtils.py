import os
import difflib
from glob import glob
from datetime import date, datetime


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

