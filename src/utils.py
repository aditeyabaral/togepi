import string
import random

def getRandomID():
    random_id = "".join(ch for ch in random.choice(string.ascii_letters+string.digits))
    return random_id


def getRepoURL(repo_name, repo_id):
    return f"https://version-control.com/{id}"