import os
import shutil


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
        print("Error while creating directory.")


def rmdir(dirname):
    cur_path = os.getcwd()
    path = os.path.join(cur_path, dirname)
    try:
        shutil.rmtree(path)
    except:
        print("Error while deleting directory.")


def cd(path):
    try:
        os.chdir(path)
    except OSError:
        print("Error while changing path.")
