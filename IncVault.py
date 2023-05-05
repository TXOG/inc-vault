try:
    from os.path import exists
    import os
    import bcrypt
    from tkinter import filedialog
    import shutil
    import hashlib
    import pathlib
    from cryptography.fernet import Fernet
    from pathlib import Path
    import base64
    import atexit
    import time
    import glob
    import hmac
    from pyargon2 import hash
    import getpass
except Exception as e:
    file = open('logs/error.log', 'a')
    errormsg = (str(e) + str('\n'))
    file.write(errormsg)
    file.close()
    try:
        os.system("pipinstalls.bat")
        time.sleep(5)
        os.system('cls||clear')
    except Exception as e:
        print("An unknown error occurred - check logs/error.log")
        file = open('logs/error.log', 'a')
        errormsg = (str(e) + str('\n'))
        file.write(errormsg)
        file.close()

try:
    from commands.addcmd import addcmd
    from commands.closecmd import closecmd
    from commands.delaccountcmd import deleteaccountcmd
    from commands.helpcmd import helpcmd
    from commands.listcmd import listcmd
    from commands.opencmd import opencmd
    from commands.purgecmd import purgecmd
    from commands.removecmd import removecmd
    from commands.renamecmd import renamecmd
    from commands.exportcmd import exportcmd
    from commands.exportpurgecmd import purgeexportcmd
    from commands.security.hashfile import hashfile
    from commands.security.encryptions import *
    from commands.error.finishedprocess import finishedprocess

except Exception as e:
    print("You are missing a command, exiting in 10 seconds")
    file = open('logs/error.log', 'a')
    errormsg = (str(e) + str('\n'))
    file.write(errormsg)
    file.close()
    time.sleep(10)
    exit()


initialdir = pathlib.Path(__file__).parent.absolute()
lockerdir = (str(initialdir) + str('/locker'))

if not os.path.exists('logs/error.log'):
    file = open('logs/error.log', 'w+')
    file.close()

if os.path.getsize('logs/error.log') > 1000000:
    file = open('logs/error.log', 'w+')
    file.seek(0)
    file.truncate(0)
    file.close()



def exit_handler():
    print("Exiting")
    file = open('openfile.ivd', 'r+')
    canexit = file.read()
    file.close()
    if not hmac.compare_digest(canexit, "NONE"):
        filename = pathlib.Path(canexit).stem
        namefile = (str(filename) + str('.ivd'))
        file = open(namefile, 'r+')
        type = file.read()
        file.close()
        if hmac.compare_digest(type, "sp"):
            print(
                "A file can't be closed as it has a second password, please reopen the application and close this file")
            print("Closing in 10 seconds")
            time.sleep(10)
        else:
            print("Looks like you didn't close a file, closing it now")
            closecmd()


atexit.register(exit_handler)


def setup():
    global password
    print("Doing first time setup")
    policy = False
    while policy == False:
        password = getpass.getpass(prompt='Enter password: ')
        if len(password) < 8:
            print("Password too short (min 8 characters)")
        elif not (any(char.isalpha() for char in password) and any(char.isdigit() for char in password) and any(
                not char.isalnum() for char in password)):
            print("Password must have at least 1 number and 1 symbol")
        else:
            policy = True

    hashed = hashfile(to_hash=password)
    file = open('password.ivp', 'w+')
    writehashed = str(hashed)
    file.write(writehashed)
    file.close()
    newpath = r'./locker'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    file = open('setupdone.ivd', 'w+')
    file.close()
    file = open('openfile.ivd', 'w+')
    file.write("NONE")
    file.close()
    os.system('cls||clear')


def check_setup():
    global password
    if exists('setupdone.ivd'):
        global passnotcorrect
        passnotcorrect = True
        while passnotcorrect:
            password = getpass.getpass(prompt='Enter password: ')
            file = open('password.ivp', 'r')
            checkhash = file.read()
            file.close()
            passwordcheck = hashfile(to_hash=password)
            if hmac.compare_digest(str(passwordcheck), str(checkhash)):
                passnotcorrect = False
                os.system('cls||clear')
            else:
                print("Password is incorrect \n")

    else:
        setup()


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
    if not hmac.compare_digest(fileopen, "NONE"):
        print("Looks like a file was left open, closing it now")
        closecmd(password=password, initialdir=initialdir, lockerdir=lockerdir)
    print("\n")
except Exception as e:
    file = open('logs/error.log', 'a')
    errormsg = (str(e) + str('\n'))
    file.write(errormsg)
    file.close()
    print("\n")
print(
    "Enter help for full list of commands \nRemember to close the last file before exiting \nPlease only exit using the"
    " command exit")


def process_command(commandinput):
    commands = {
        "add": ("addcmd", {"password": password, "initialdir": initialdir, "lockerdir": lockerdir}),
        "open": ("opencmd", {"password": password, "initialdir": initialdir, "lockerdir": lockerdir, "prevcmd": "NONE"}),
        "close": ("closecmd", {"password": password, "initialdir": initialdir, "lockerdir": lockerdir}),
        "help": ("helpcmd", {}),
        "remove": ("removecmd", {"password": password, "initialdir": initialdir, "lockerdir": lockerdir}),
        "list": ("listcmd", {"lockerdir": lockerdir}),
        "rename": ("renamecmd", {"initialdir": initialdir, "lockerdir": lockerdir}),
        "delaccount": ("deleteaccountcmd", {"initialdir": initialdir, "lockerdir": lockerdir}),
        "export": ("exportcmd", {"password": password, "initialdir": initialdir, "lockerdir": lockerdir}),
        "purgeexport": ("purgeexportcmd", {"initialdir": initialdir}),
    }

    for command, (function, kwargs) in commands.items():
        if hmac.compare_digest(command, commandinput):
            globals()[function](**kwargs)
            return True

    return False


while True:
    commandinput = input(">> ").lower()
    if hmac.compare_digest(commandinput, "exit"):
        exit()
    elif hmac.compare_digest(commandinput, "purgelocker"):
        rusure = input("Are you sure you want to purge your locker(y/n) ")
        purgecmd(rusure=rusure, lockerdir=lockerdir, initialdir=initialdir)
    elif not process_command(commandinput):
        print("Oops that's not a command \nUse help for a full list of commands")
