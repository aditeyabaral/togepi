import string
import random
import shutil
import os


'''def getRandomID():
    random_id = "".join(ch for ch in random.choice(
        string.ascii_letters+string.digits))
    return random_id


def getRepoURL(repo_name, repo_id):
    return f"https://version-control.com/{id}"'''


def nano(filename):
    os.system(f"nano {filename}")


def cat(filename):
    os.system(f"cat {filename}")


def ls(path="."):
    print("\n".join(os.listdir(path)))


def mkdir(dirname):
    cur_path = os.getcwd()
    path = os.path.join(cur_path, dirname)
    try:
        os.mkdir(path)
    except:
        print("Error while creating directory!")

def rmdir(dirname):
    cur_path = os.getcwd()
    path = os.path.join(cur_path, dirname)
    try:
        shutil.rmtree(path)
    except:
        print("Error while deleting directory!")


def cd(path):
    try:
        os.chdir(path)
    except OSError:
        print("Error while changing path")
