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