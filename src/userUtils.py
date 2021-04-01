import dbUtils
import fsUtils
import validationUtils


def generateUserID():
    all_users = dbUtils.getAllUserID()
    if not all_users:
        user_id = "USER#000001"
    else:
        roll_numbers = sorted([int(i[0][5:]) for i in all_users])
        new_roll_number = str(roll_numbers[-1] + 1)
        user_id = f"USER#{new_roll_number.zfill(6)}"
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
        password = input("Enter password: ")
        if validationUtils.validatePassword(password):
            break
    _id = generateUserID()
    print(f"Creating ID: {_id}")
    dbUtils.createUser(_id, username, email, password)
    fsUtils.createFolder(username)
    return _id


def loginUser(username, password):
    user_id = dbUtils.checkUserCredentials(username, password)
    return user_id
