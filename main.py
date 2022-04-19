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
try:
    file = open('openfile.ivd', 'r+')
    fileopen = file.read()
    file.close()
    if fileopen != ("NONE"):
        print("Looks like a file was left open, closing it now")
        closecmd()
    print("\n")
except:
    print("\n")
print("Enter help for full list of commands \nRemember to close the last file before exiting \nPlease only exit using the command exit")
while True:
    vcommand = False
    commandinput = input(">> ")
    commandinput = str(commandinput)
    commandinput.lower()
    if commandinput == ("exit"):
        vcommand = True
        exitcmd()
    if commandinput == ("add"):
        vcommand = True
        addcmd()
    if commandinput == ("open"):
        vcommand = True
        opencmd()
    if commandinput == ("close"):
        vcommand = True
        closecmd()
    if commandinput == ("help"):
        vcommand = True
        helpcmd()
    if commandinput == ("remove"):
        vcommand = True
        removecmd()
    if commandinput == ("list"):
        vcommand = True
        listcmd()
    if vcommand == False:
        print("Oops that's not a command \nUse help for a full list of commands")
    else:
        vcommand = False
