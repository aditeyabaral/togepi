from os.path import isfile
import dropbox
import os
import dotenv
from glob import glob


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
    for entry in dbx.files_list_folder(dropbox_path).entries:
        print(entry.name)


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

    for file in files:
        rel_path = os.path.relpath(file, local_path)
        dropbox_file_path = os.path.join(dropbox_path, rel_path)
        with open(file, "rb") as f:
            print(f'Uploading {rel_path}')
            dbx.files_upload(f.read(), dropbox_file_path,
                             mode=dropbox.files.WriteMode.overwrite)
