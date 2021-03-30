import dbUtils
import fsUtils


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
    username = input("Enter username: ")    # validate
    email = input("Enter email: ")          # validate
    password = input("Enter password: ")    # validate
    _id = generateUserID()
    print(f"Creating ID: {_id}")
    dbUtils.createUser(_id, username, email, password)
    fsUtils.create_folder(_id)
    return _id


def loginUser(username, password):
    user_id = dbUtils.checkUserCredentials(username, password)
    return user_id
