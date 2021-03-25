import re
import cliUtils
import userUtils

current_user = None
current_repository = None


def checkCommandCLI(command):
    cd_command = re.compile(r"cd ([\.A-Za-z0-9\\/_]+)")
    ls_command = re.compile(r"ls ([\.A-Za-z0-9\\/_]*)")
    cat_command = re.compile(r"cat ([\.A-Za-z0-9\\/_]+)")
    nano_command = re.compile(r"nano ([\.A-Za-z0-9\\/_]+)")
    mkdir_command = re.compile(r"mkdir ([\.A-Za-z0-9\\/_]+)")
    rmdir_command = re.compile(r"rmdir ([\.A-Za-z0-9\\/_]+)")
    # add rm for files

    cli_function_mapping = {
        cd_command: cliUtils.cd,
        ls_command: cliUtils.ls,
        cat_command: cliUtils.cat,
        nano_command: cliUtils.nano,
        mkdir_command: cliUtils.mkdir,
        rmdir_command: cliUtils.rmdir,

    }

    if command == "ls":
        # handle this elegantly [LATER, NOT PRIORITY]
        return True, cli_function_mapping[ls_command], "."

    for command_type in cli_function_mapping:
        args = re.findall(command_type, command)
        if args:
            return True, cli_function_mapping[command_type], args[0]

    return False, None, None


def checkCommandUser(command):  # add log out
    user_create_command = re.compile(r"vc user create")
    user_login_command = re.compile(
        r"vc user login ([A-Za-z0-9_]*) ([A-Za-z0-9_@$]*)")

    user_function_mapping = {
        user_create_command: userUtils.createUser,
        user_login_command: userUtils.loginUser
    }

    if command == "vc user create":
        return True, userUtils.createUser, None

    args = re.findall(user_login_command, command)
    if args:
        return True, userUtils.loginUser, args[0]

    return False, None, None


def runCommand(command):

    global current_user
    global current_repository

    '''
        vc add .
        vc add file1 file2 ...
        vc commit -m "message"
        vc commit -am "message"
        vc push
        vc pull
        vc init repo_name
    '''

    function_found, cli_command, args = checkCommandCLI(command)
    if function_found:
        cli_command(args)
        return

    function_found, user_command, args = checkCommandUser(command)
    if function_found:
        if args is None:
            user_id = user_command()
        else:
            username, password = args
            user_id = user_command(username, password)
        current_user = user_id
        return user_id
