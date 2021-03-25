import sys
import utils

current_user = None
current_repository = None

while True:
    command = input(">>> ")
    if command == "exit":
        sys.exit(0)
    else:
        result = utils.runCommand(command)
        if result is not None and result.startswith("USER"):
            current_user = result
