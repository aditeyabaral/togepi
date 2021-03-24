import string
import random
import os


def getRandomID():
    random_id = "".join(ch for ch in random.choice(
        string.ascii_letters+string.digits))
    return random_id


def getRepoURL(repo_name, repo_id):
    return f"https://version-control.com/{id}"


def nano(filename):
    os.system(f"micro {filename}")


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


def cd(path):
    try:
        os.chdir(path)
    except (WindowsError, OSError):
        print("Error while changing path")
