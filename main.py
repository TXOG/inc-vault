from functions import *
import os


check_setup()

print("""  _____         __      __         _ _
 |_   _|        \ \    / /        | | |
   | |  _ __   __\ \  / /_ _ _   _| | |_
   | | | '_ \ / __\ \/ / _` | | | | | __|
  _| |_| | | | (__ \  / (_| | |_| | | |_
 |_____|_| |_|\___| \/ \__,_|\__,_|_|\__|

                                         """)
print("Enter help for full list of commands \nRemember to close the last file before exiting")
while True:
    commandinput = input(">> ")
    commandinput = str(commandinput)
    commandinput.lower()
    if commandinput == ("exit"):
        exitcmd()
    if commandinput == ("add"):
        addcmd()
    if commandinput == ("open"):
        opencmd()
    if commandinput == ("close"):
        closecmd()
    if commandinput == ("help"):
        helpcmd()
