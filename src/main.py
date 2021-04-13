import sys
import utils
from cliUtils import togepi

print("Welcome to Togepi!")
togepi()

DEBUG=False
if sys.argv[1] == "debug":
    DEBUG = True

while True:
    command = input(">>> ")
    if command == "exit":
        sys.exit(0)
    else:
        try:
            utils.runCommand(command)
        except Exception as e:
            if DEBUG:
                print(e)
            else:
                print("Invalid command. Type help to learn more.\nYou can also visit https://github.com/aditeyabaral/togepi#how-to-use-togepi to read the entire documentation.")
