import sys
import utils


while True:
    command = input(">>> ")
    if command == "exit":
        sys.exit(0)
    else:
        utils.runCommand(command)
