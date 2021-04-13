import getpass
from dbUtils import userDBUtils
import fsUtils
import validationUtils

userDB = userDBUtils()


def generateUserID():
    all_users = userDB.getAllUserID()
    if not all_users:
        user_id = "USER000001"
    else:
        roll_numbers = sorted([int(i[0][5:]) for i in all_users])
        new_roll_number = str(roll_numbers[-1] + 1)
        user_id = f"USER{new_roll_number.zfill(6)}"
    return user_id


def createUser():
    while True:
        username = input("Enter username: ")
        if validationUtils.validateUsername(username):
            break
    while True:
        email = input("Enter email: ")
        if validationUtils.validateEmail(email):
            break
    while True:
        # input("Enter password: ")
        password = getpass.getpass("Enter password: ")
        if validationUtils.validatePassword(password):
            break
    user_id = generateUserID()
    print(f"Creating ID: {user_id}")
    userDB.createUser(user_id, username, email, password)
    fsUtils.createFolder(username)
    return user_id, username


def createUserGUI(user_id, username, password, email):
    userDB.createUser(user_id, username, email, password)
    fsUtils.createFolder(username)
    return user_id, username


def askLoginCredentials():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    return username, password


def loginUser(credentials=None):
    if credentials is None:
        username, password = askLoginCredentials()
    else:
        username, password = credentials
    user_id = userDB.checkUserCredentials(username, password)
    if user_id is None:
        username = None
    return user_id, username
