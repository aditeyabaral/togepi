import sys
import utils
from cliUtils import togepi

print("Welcome to Togepi!")
togepi()

while True:
    command = input(">>> ")
    if command == "exit":
        sys.exit(0)
    else:
        try:
            utils.runCommand(command)
        except Exception as e:
            print(e)
