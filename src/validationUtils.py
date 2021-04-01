import re
import dbUtils


def validateUsername(username):
    usernameRegex = re.compile(r"^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$")
    validUsername = bool(re.findall(usernameRegex, username))
    if not validUsername:
        print("Invalid username! Username cannot contain special characters at the beginning or end, or consecutively!")
        return False
    allUsernames = dbUtils.getAllUsername()
    if username in allUsernames[0]:
        print("Sorry, that username already exists! Please try another one")
        return False
    else:
        return True


def validatePassword(password):
    pwdRegex = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
    validPwd = bool(re.findall(pwdRegex, password))
    if not validPwd:
        print("Invalid password! Must be more than 8 chars long and have atleast one number and letter!")
        return False
    return True


def validateEmail(email):
    emailRegex = re.compile(r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$")
    validEmail = bool(re.findall(emailRegex, email))
    if not validEmail:
        print("Invalid email! Email must contain an @ character and can only have _.- as special chars!")
        return False
    return True
