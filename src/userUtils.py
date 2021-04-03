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
    user_id = generateUserID()
    print(f"Creating ID: {user_id}")
    dbUtils.createUser(user_id, username, email, password)
    fsUtils.createFolder(username)
    return user_id, username


def loginUser(username, password):
    # Check if credentials are right -- return values based on that
    user_id = dbUtils.checkUserCredentials(username, password)
    if user_id is None:
        username = None
    return user_id, username
