from os.path import isfile
import dropbox
import os
import dotenv
from glob import glob
from datetime import datetime
import zipfile
import cliUtils

dotenv.load_dotenv()
dbx = dropbox.Dropbox(os.environ["DROPBOX_ACC_TOK"])


def downloadFile(local_path, dropbox_path):
    metadata, f = dbx.files_download(dropbox_path)
    out = open(local_path, 'w')
    cont = f.content.decode()
    out.write(cont)
    out.close()


def getContent(dropbox_path):
    try:
        metadata, f = dbx.files_download(dropbox_path)
        cont = f.content.decode()
    except:
        cont = ""
    return cont


def uploadFile(local_path, dropbox_path):
    text = open(local_path, "rb").read()
    dbx.files_upload(text, dropbox_path)


def ls_dropbox(dropbox_path=""):
    print("LS dropbox:", dropbox_path)
    files = list()
    for entry in dbx.files_list_folder(dropbox_path).entries:
        #print(entry.name)
        files.append(entry.name)
    return files


def createFolder(dropbox_path):
    if not dropbox_path.startswith("/"):
        dropbox_path = "/"+dropbox_path
    dbx.files_create_folder(dropbox_path)


def uploadFolder(local_path, dropbox_path):
    files = [
        os.path.join(parent, name)
        for (parent, subdirs, files) in os.walk(local_path)
        for name in files + subdirs
    ]

    files = [fname for fname in files if os.path.isfile(fname)]
    output_str = []
    for file in files:
        rel_path = os.path.relpath(file, local_path)
        dropbox_file_path = os.path.join(dropbox_path, rel_path)
        with open(file, "rb") as f:
            print(f'Uploading {rel_path}')
            if not rel_path.startswith(".togepi"):
                output_str.append(f'Uploaded {rel_path}')
            dbx.files_upload(f.read(), dropbox_file_path,
                             mode=dropbox.files.WriteMode.overwrite)
    return output_str


def getRecentCloudCommitTime(dropbox_path):
    all_commits = ls_dropbox(dropbox_path)
    all_commits.remove("tgpinfo.txt")
    if all_commits:
        times = list(map(lambda x: x.split('--')[-1], all_commits))
        times = list(map(lambda x: datetime.strptime(
            x, "%Y-%m-%d-%H:%M:%S"), times))
        return times[-1]
    return None


def getRecentLocalCommitTime():
    all_commits = os.listdir(".togepi/")
    all_commits.remove("tgpinfo.txt")
    if all_commits:
        times = list(map(lambda x: x.split('--')[-1], all_commits))
        times = list(map(lambda x: datetime.strptime(
            x, "%Y-%m-%d-%H:%M:%S"), times))
        return times[-1]
    return None


def downloadFolder(username, repo_name, pull=True):
    if pull:
        cliUtils.cd("..")
    local_path = os.getcwd()
    dropbox_path = f"/{username}/{repo_name}"
    try:
        local_zip_path = local_path + f"/{repo_name}.zip"
        dbx.files_download_zip_to_file(local_zip_path, dropbox_path)
        os.system(f"unzip -o {repo_name}.zip")
        os.remove(f"{repo_name}.zip")
        if pull:
            cliUtils.cd(f"{repo_name}")
    except:
        print("Could not pull. Error occured.")