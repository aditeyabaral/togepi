import sys
import utils


while True:
    command = input(">>> ")
    if command == "exit":
        sys.exit(0)
    else:
        try:
            utils.runCommand(command)
        except Exception as e:
            print(e)
