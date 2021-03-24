import re
import cliUtils
import userUtils


def runCommand(command):
    '''
        vc user create
        vc user login username password
        vc add .
        vc add file1 file2 ...
        vc commit -m "message"
        vc commit -am "message"
        vc push
        vc pull
        vc init repo_name
    '''

    cd_command = re.compile(r"cd ([\.A-Za-z0-9\\/_]+)")
    ls_command = re.compile(r"ls ([\.A-Za-z0-9\\/_]*)")
    cat_command = re.compile(r"cat ([\.A-Za-z0-9\\/_]+)")
    nano_command = re.compile(r"nano ([\.A-Za-z0-9\\/_]+)")
    mkdir_command = re.compile(r"mkdir ([\.A-Za-z0-9\\/_]+)")
    rmdir_command = re.compile(r"rmdir ([\.A-Za-z0-9\\/_]+)")

    user_create_command = re.compile(r"vc user create")
    user_login_command = re.compile(
        r"vc user login ([A-Za-z0-9_]*) ([A-Za-z0-9_@$]*)")

    cli_function_mapping = {
        cd_command: cliUtils.cd,
        ls_command: cliUtils.ls,
        cat_command: cliUtils.cat,
        nano_command: cliUtils.nano,
        mkdir_command: cliUtils.mkdir,
        rmdir_command: cliUtils.rmdir,

    }

    user_function_mapping = {
        user_create_command: userUtils.createUser,
        user_login_command: userUtils.loginUser
    }

    for command_type in cli_function_mapping:
        args = re.findall(command_type, command)
        if args:
            cli_function_mapping[command_type](args[0])
            return
        elif command == "ls":   # handle this elegantly
            cli_function_mapping[ls_command](".")
            return
        else:
            pass

    if command == "vc user create":
        user_id = userUtils.createUser()
        return user_id

    args = re.findall(command_type, command)
    if args:
        username, password = args[0]
        user_id = userUtils.loginUser(username, password)
        return user_id

    return None, None
