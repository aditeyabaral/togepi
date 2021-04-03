import os
import re
import cliUtils
import userUtils
import repoUtils

# current_user = None
# current_repository_id = None
# current_repository_name = None

cache = {
    "current_user_id": None,
    "current_username": None,
    "current_repository_id": None,
    "current_repository_name": None
}


def setGlobalUserDetails():
    global cache
    # nothing to see here, move along


def setGlobalRepositoryDetails():
    global cache
    if ".togepi" in os.listdir():
        with open(".togepi/info.txt") as f:
            content = f.read().strip().split('\n')
            _, current_repository_id = content[0].split(',')
            current_repository_id = current_repository_id.strip()

            _, current_repository_name = content[1].split(',')
            current_repository_name = current_repository_name.strip()
        cache["current_repository_id"] = current_repository_id
        cache["current_repository_name"] = current_repository_name


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
        return True, cliUtils.help, None

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

    if command == "tgp user logout":
        pass
        # do something here

    if command == "tgp user create":
        return True, userUtils.createUser, None

    args = re.findall(user_login_command, command)
    if args:
        return True, userUtils.loginUser, args[0]

    return False, None, None


def checkCommandRepository(command):
    create_repo_command = re.compile(r"tgp init ([A-Za-z0-9_]*)")
    add_files_command = re.compile(r"tgp add (( *[A-Za-z0-9._]*)*)")
    commit_files_command = re.compile(r"tgp commit ([A-Za-z0-9_]*)")

    repo_function_mapping = {
        create_repo_command: repoUtils.init,
        add_files_command: repoUtils.add,
        commit_files_command: repoUtils.commit
    }

    if command == "tgp push":
        return True, repoUtils.push, None

    for command_type in repo_function_mapping:
        args = re.findall(command_type, command)
        if args:
            if command_type == add_files_command:
                args = args[0]
            return True, repo_function_mapping[command_type], args[0]


def runCommand(command):

    # global current_user
    # global current_repository_id
    # global current_repository_name
    global cache
    # print(cache)

    function_found, cli_command, args = checkCommandCLI(command)
    if function_found:
        cli_command(args)
        setGlobalRepositoryDetails()
        # if ".togepi" in os.listdir():
        #     with open(".togepi/info.txt") as f:
        #         content = f.read().strip().split('\n')
        #         _, current_repository_id = content[0].split(',')
        #         current_repository_id = current_repository_id.strip()
        #         _, current_repository_name = content[1].split(',')
        #         current_repository_name = current_repository_name.strip()
        return

    function_found, user_command, args = checkCommandUser(command)
    if function_found:
        if args is None:
            user_id, username = user_command()
        else:
            username, password = args
            user_id, username = user_command(username, password)
        cache["current_user_id"] = user_id
        cache["current_username"] = username
        return

    function_found, repo_command, args = checkCommandRepository(command)
    if cache["current_user_id"] is None:
        print("Please login before performing repository functions.")
    else:
        if function_found:
            # if repo_command == repoUtils.add:
            #     repoUtils.add(current_user, current_repository_id, args)
            # elif repo_command == repoUtils.push:
            #     repoUtils.push(current_user, current_repository_name)
            # else:
            #     repo_command(current_user, current_repository_name, args)
            if args is None:
                repo_command(cache)
            else:
                repo_command(cache, args)
