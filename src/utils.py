import os
import re
import cliUtils
import userUtils
import repoUtils

current_user = None
current_repository = None


def help(*vargs):
    content = '''TOGEPI

Togepi is a command line based version control system built using Python3 and Google Drive API

1. User Commands

tgp create user -- Create an account
tgp user login username password -- Login to existing account

2. Repository Commands

tgp init repository_name -- Create a new repository

3. CLI tools

You can invoke other CLI commands such as -- 

cd
ls
cat
nano
rmdir
mkdir'''
    print(content)


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

    if command == "help":
        return True, help, None

    if command == "ls":
        # handle this elegantly [LATER, NOT PRIORITY]
        return True, cli_function_mapping[ls_command], "."

    for command_type in cli_function_mapping:
        args = re.findall(command_type, command)
        if args:
            return True, cli_function_mapping[command_type], args[0]

    return False, None, None


def checkCommandUser(command):  # add log out
    user_create_command = re.compile(r"tgp user create")
    user_login_command = re.compile(
        r"tgp user login ([A-Za-z0-9_]*) ([A-Za-z0-9_@$]*)")

    user_function_mapping = {
        user_create_command: userUtils.createUser,
        user_login_command: userUtils.loginUser
    }

    if command == "tgp user create":
        return True, userUtils.createUser, None

    args = re.findall(user_login_command, command)
    if args:
        return True, userUtils.loginUser, args[0]

    return False, None, None


def checkCommandRepository(command):
    create_repo_command = re.compile(r"tgp init ([A-Za-z0-9_]*)")
    add_files_command = re.compile(r"tgp add (( *[A-Za-z0-9._]*)*)")

    repo_function_mapping = {
        create_repo_command: repoUtils.init,
        add_files_command: repoUtils.add
    }

    for command_type in repo_function_mapping:
        args = re.findall(command_type, command)
        if args:
            if command_type == add_files_command:
                args = args[0]
            return True, repo_function_mapping[command_type], args[0]


def runCommand(command):

    global current_user
    global current_repository

    '''
        tgp add .
        tgp add file1 file2 ...
        tgp commit -m "message"
        tgp push
        tgp pull
    '''

    function_found, cli_command, args = checkCommandCLI(command)
    if function_found:
        cli_command(args)
        if ".togepi" in os.listdir():
            with open(".togepi/info.txt") as f:
                content = f.read().strip().split('\n')
                _, current_repository = content[0].split(',')
                current_repository = current_repository.strip()
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

    function_found, repo_command, args = checkCommandRepository(command)
    if current_user is None:
        print("Please login before performing repository functions.")
    else:
        if function_found:
            if repo_command == repoUtils.add:
                repoUtils.add(current_user, current_repository, args)
            else:
                repo_command(current_user, args)
