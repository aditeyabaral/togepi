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
    files = [y for x in os.walk(local_path)
             for y in glob(os.path.join(x[0], '*.*'))]
    for file in files:
        rel_path = os.path.relpath(file, local_path)
        dropbox_file_path = os.path.join(dropbox_path, rel_path)
        with open(file, "rb") as f:
            print(f'Uploading {rel_path}')
            dbx.files_upload(f.read(), dropbox_file_path)
