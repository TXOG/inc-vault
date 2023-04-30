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
        print("An unknown error occured - check logs/error.log")
        file = open('logs/error.log', 'a')
        errormsg = (str(e) + str('\n'))
        file.write(errormsg)
        file.close()


def listcmd():
    global lockerdir
    print(os.listdir(lockerdir))


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

global custompass
global filepath
global data
global salt
global extension
global initialdir
global lockerdir

data = ''
extension = ''
salt = ''
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


def hashfile(to_hash):
    argonhash = str(hash(to_hash, "123456789123456789"))
    argonhash = argonhash.encode('utf-8')
    return hashlib.sha256(argonhash).digest()



def removecmd():
    closecmd()
    couldntremove = ("NONE")
    filepath = filedialog.askopenfilename(initialdir="./locker",
                                          title="Select a File",
                                          filetypes=(("all files",
                                                      "*.*"),
                                                     ("all files",
                                                      "*.*")))
    rusure = input("Are you sure you want to remove this file(y/n): ")
    rusure = rusure.lower()
    if hmac.compare_digest(rusure, "y"):
        try:
            filename = pathlib.Path(filepath).stem
            couldntremove = (filename)
            os.remove(filepath)
            namefile = (str(filename) + str(".ive"))
            couldntremove = (namefile)
            os.remove(namefile)
            namefile = (str(filename) + str(".ivd"))
            couldntremove = (namefile)
            os.remove(namefile)
            namefile = (str(filename) + str(".ivs"))
            couldntremove = (namefile)
            os.remove(namefile)
            print("Successfully removed file")
        except Exception as e:
            print("There was an error removing file")
            print("Couldn't remove:")
            print(couldntremove)
            file = open('logs/error.log', 'a')
            errormsg = (str(e) + str('\n'))
            file.write(errormsg)
            file.close()
    else:
        print("Cancelled")


def helpcmd():
    print(
        "Here's a list of all commands that are avaliable at the moment: \n \nadd: Adds a file to the system \nclose: Closes the last file opened (don't forget to do this before exiting) \ndelaccount: Purge locker and reset application \nexit: Exits the program \nhelp: Shows this message :) \nlist: Lists all the files in your locker \nopen: Opens a file selected from a gui \npurge: Deletes all files in your locker \nremove: Deletes a file selected from a gui \nrename: Renames selected file")


def finishedprocess():
    print("The process was terminated due to an error")
    return


def closecmd():
    global custompass
    global password
    global filepath
    global data
    global salt
    global extension
    global initialdir
    global lockerdir

    try:
        file = open('openfile.ivd', 'r+')
        mostrecentpath = file.read().strip()
        file.close()

        if hmac.compare_digest(mostrecentpath, "NONE"):
            print("All files are closed")
            finishedprocess()
        else:
            filename = pathlib.Path(mostrecentpath).stem
            fullfilename = os.path.basename(mostrecentpath).strip()

            namefile = (str(filename) + str(".ive"))
            file = open(namefile, 'r+')
            extension = file.read()
            file.close()
            namefile = (str(filename) + str(".ivd"))
            file = open(namefile, 'r+')
            data = file.read()
            file.close()
            namefile = (str(filename) + str(".ivs"))
            file = open(namefile, 'r+')
            salt = file.read()
            file.close()

            if hmac.compare_digest(data, "sp"):
                # gets the user to input their password
                custompass = getpass.getpass(prompt='Enter password a new password for this file: ')
                # adds password and salt together - then encodes
                passnsalt = (str(custompass) + str(salt))
                # hashes the password and salt to use as a key
                hashed = hashfile(to_hash=passnsalt)
                key = base64.urlsafe_b64encode(hashed)
                # creates fernet so encryption can happen
                fernet = Fernet(key)
                # gets new file path
                # gets the bytes data of a file and encrypts
                os.chdir(lockerdir)
                with open(fullfilename, "rb") as file:
                    file_data = file.read()
                    encrypted_data = fernet.encrypt(file_data)
                    file.close()
                # writes to the binary of a file
                with open(fullfilename, "wb") as file:
                    file.write(encrypted_data)
                    file.close()
                os.chdir(initialdir)
                originalpassnsalt = (str(password) + str(salt))
                # hashes the password and salt to use as a key
                hashed = hashfile(to_hash=originalpassnsalt)
                key = base64.urlsafe_b64encode(hashed)
                # creates fernet so encryption can happen
                fernet = Fernet(key)
                # gets the bytes data of a file and encrypts
                os.chdir(lockerdir)
                with open(fullfilename, "rb") as file:
                    file_data = file.read()
                    encrypted_data = fernet.encrypt(file_data)
                    file.close()
                # writes to the binary of a file
                with open(fullfilename, "wb") as file:
                    file.write(encrypted_data)
                    file.close()
                newfilename = (str(filename) + str('.ivf'))
                os.rename(fullfilename, newfilename)
                os.chdir(initialdir)
            else:
                originalpassnsalt = (str(password) + str(salt))
                # hashes the password and salt to use as a key
                hashed = hashfile(to_hash=originalpassnsalt)
                key = base64.urlsafe_b64encode(hashed)
                # creates fernet so encryption can happen
                fernet = Fernet(key)
                # gets the bytes data of a file and encrypts
                os.chdir(lockerdir)
                with open(fullfilename, "rb") as file:
                    file_data = file.read()
                    encrypted_data = fernet.encrypt(file_data)
                    file.close()
                # writes to the binary of a file
                with open(fullfilename, "wb") as file:
                    file.write(encrypted_data)
                    file.close()
                newfilename = (str(filename) + str('.ivf'))
                os.rename(fullfilename, newfilename)
                os.chdir(initialdir)
            file = open('openfile.ivd', 'w+')
            file.truncate(0)
            file.write("NONE")
            file.close()
            print("File closed successfully")


    except Exception as e:
        print("There was an error while trying to close this file")
        file = open('logs/error.log', 'a')
        errormsg = (str(e) + str('\n'))
        file.write(errormsg)
        file.close()
        finishedprocess()
        return


def opencmd():
    global password
    global custompass
    global filepath
    global salt
    global data
    global extension
    global initialdir
    global lockerdir

    file = open('openfile.ivd', 'r+')
    mostrecentpath = file.read().strip()
    file.close()

    if not hmac.compare_digest(mostrecentpath, "NONE"):
        print("Please close the last file you opened with the command: close")
        finishedprocess()
    else:

        filepath = filedialog.askopenfilename(initialdir="./locker",
                                              title="Select a File",
                                              filetypes=(("all files",
                                                          "*.*"),
                                                         ("all files",
                                                          "*.*")))
        # find filename without extension
        filename = pathlib.Path(filepath).stem

        fullfilename = os.path.basename(filepath)

        try:
            namefile = (str(filename) + str(".ive"))
            os.chdir(initialdir)
            file = open(namefile, 'r+')
            extension = file.read()
            file.close()
            namefile = (str(filename) + str(".ivd"))
            file = open(namefile, 'r+')
            data = file.read()
            file.close()
            namefile = (str(filename) + str(".ivs"))
            file = open(namefile, 'r+')
            salt = file.read()
            file.close()
        except Exception as e:
            print("One or more files don't exist, to open you must restore them")
            file = open('logs/error.log', 'a')
            errormsg = (str(e) + str('\n'))
            file.write(errormsg)
            file.close()
            finishedprocess()
            return

        # Seeing if there is a seperate password
        if hmac.compare_digest(data, "sp"):
            shutil.copy(filepath, initialdir)
            backuppath = (str(initialdir) + str('/') + str(fullfilename))
            backupfullfilename = os.path.basename(backuppath)
            try:
                # getting custom password
                custompass = getpass.getpass(prompt='Enter password: ')
                # decrypting with orignial password first
                passnsalt = (str(password) + str(salt))
                hash = hashfile(to_hash=passnsalt)
                key = base64.urlsafe_b64encode(hash)
                fernet = Fernet(key)
                with open(filepath, "rb") as file:
                    file_data = file.read()
                    decrypted_data = fernet.decrypt(file_data)
                    file.close()
                # writes to the binary of a file
                with open(filepath, "wb") as file:
                    file.write(decrypted_data)
                    file.close()
                # decrypting with new differnet password
                cpassnsalt = (str(custompass) + str(salt))
                hash = hashfile(to_hash=cpassnsalt)
                key = base64.urlsafe_b64encode(hash)
                fernet = Fernet(key)
                with open(filepath, "rb") as file:
                    file_data = file.read()
                    decrypted_data = fernet.decrypt(file_data)
                    file.close()
                # writes to the binary of a file
                with open(filepath, "wb") as file:
                    file.write(decrypted_data)
                    file.close()
                # rename the file
                revertfilename = (str(filename) + str(extension))
                os.chdir(lockerdir)
                os.rename(filepath, revertfilename)
                os.chdir(initialdir)
                # open in defualt application
                path2open = (str(lockerdir) + str('/')
                             + str(filename) + str(extension))
                os.remove(backupfullfilename)
                os.startfile(path2open)
            except Exception as e:
                print(
                    "There was an error while opening this file, maybe you used the wrong password?")
                file = open('logs/error.log', 'a')
                errormsg = (str(e) + str('\n'))
                file.write(errormsg)
                file.close()
                os.chdir(lockerdir)
                os.remove(backupfullfilename)
                os.chdir(initialdir)
                shutil.copy(backuppath, lockerdir)
                os.remove(backupfullfilename)
                finishedprocess()
                return
        else:
            try:
                # decrypting with orignial password
                passnsalt = (str(password) + str(salt))
                hash = hashfile(to_hash=passnsalt)
                key = base64.urlsafe_b64encode(hash)
                fernet = Fernet(key)
                with open(filepath, "rb") as file:
                    file_data = file.read()
                    decrypted_data = fernet.decrypt(file_data)
                    file.close()
                # writes to the binary of a file
                with open(filepath, "wb") as file:
                    file.write(decrypted_data)
                    file.close()
                revertfilename = (str(filename) + str(extension))
                os.chdir(lockerdir)
                os.rename(filepath, revertfilename)
                os.chdir(initialdir)
                # open in defualt application
                path2open = (str(lockerdir) + str('/')
                             + str(filename) + str(extension))
                os.startfile(path2open)
            except Exception as e:
                print("There was error while trying to open the file")
                file = open('logs/error.log', 'a')
                errormsg = (str(e) + str('\n'))
                file.write(errormsg)
                file.close()
                finishedprocess()
                return
        file = open('openfile.ivd', 'w+')
        namefile = (str(filename) + str(extension))
        file.write(namefile)
        file.close()


def exitcmd():
    exit()


def addcmd():
    try:
        global password
        global data
        global extension
        global salt
        global lockerdir
        global initialdir
        # gui to choose files
        filepath = filedialog.askopenfilename(initialdir="C:/",
                                              title="Select a File",
                                              filetypes=(("all files",
                                                          "*.*"),
                                                         ("all files",
                                                          "*.*")))
        if not filepath:
            return
        # find file extension
        file_extension = pathlib.Path(filepath).suffix
        # find filename without extension
        filename = pathlib.Path(filepath).stem
        # find file name with extenion
        fullfilename = os.path.basename(filepath)
        # writes file extension to file
        namefile = (str(filename) + str('.ive'))
        file = open(namefile, 'w+')
        file.write(file_extension)
        file.close()
        # moves file to locker folder
        shutil.move(filepath, "./locker")
        # allows user to choose if custom password for this specific file
        newpass = input(
            "Do you want to have a seperate password for this file(y/n): ")
        newpass.lower()
        if hmac.compare_digest(newpass, "y"):
            invalidinput = False
        elif hmac.compare_digest(newpass, "n"):
            invalidinput = False
        else:
            invalidinput = True
        if hmac.compare_digest(newpass, "y"):
            # writes to a file that seperate password
            namefile = (str(filename) + str('.ivd'))
            file = open(namefile, 'w+')
            file.write("sp")
            file.close()
            # generates a random salt
            salt = bcrypt.gensalt()
            # gets the user to input their password
            custompass = getpass.getpass(prompt='Enter password for this file: ')
            # adds password and salt together - then encodes
            passnsalt = (str(custompass) + str(salt))
            # writes the salt to a file
            namefile = (str(filename) + str('.ivs'))
            file = open(namefile, 'w+')
            file.write(str(salt))
            file.close()
            # hashes the password and salt to use as a key
            hashed = hashfile(to_hash=passnsalt)
            key = base64.urlsafe_b64encode(hashed)
            # creates fernet so encryption can happen
            fernet = Fernet(key)
            # gets new file path
            filepath = (str('./locker/') + str(filename) + str(file_extension))
            # gets the bytes data of a file and encrypts
            with open(filepath, "rb") as file:
                file_data = file.read()
                encrypted_data = fernet.encrypt(file_data)
                file.close()
            # writes to the binary of a file
            with open(filepath, "wb") as file:
                file.write(encrypted_data)
                file.close()
            originalpassnsalt = (str(password) + str(salt))
            # hashes the password and salt to use as a key
            hashed = hashfile(to_hash=originalpassnsalt)
            key = base64.urlsafe_b64encode(hashed)
            # creates fernet so encryption can happen
            fernet = Fernet(key)
            # gets the bytes data of a file and encrypts
            with open(filepath, "rb") as file:
                file_data = file.read()
                encrypted_data = fernet.encrypt(file_data)
                file.close()
            # writes to the binary of a file
            with open(filepath, "wb") as file:
                file.write(encrypted_data)
                file.close()
            os.chdir(lockerdir)
            newfilename = (str(filename) + str('.ivf'))
            os.rename(fullfilename, newfilename)
            os.chdir(initialdir)
        else:
            if invalidinput:
                print("Invalid input - using default password")
            else:
                print("Using default password")
            # writes to a file that same password
            namefile = (str(filename) + str('.ivd'))
            file = open(namefile, 'w+')
            file.write("nsp")
            file.close()
            # generates a random salt
            salt = bcrypt.gensalt()
            # writes the salt to a file
            namefile = (str(filename) + str('.ivs'))
            file = open(namefile, 'w+')
            file.write(str(salt))
            file.close()
            # gets new file path
            filepath = (str('./locker/') + str(filename) + str(file_extension))
            originalpassnsalt = (str(password) + str(salt))
            # hashes the password and salt to use as a key
            hashed = hashfile(to_hash=originalpassnsalt)
            key = base64.urlsafe_b64encode(hashed)
            # creates fernet so encryption can happen
            fernet = Fernet(key)
            # gets the bytes data of a file and encrypts
            with open(filepath, "rb") as file:
                file_data = file.read()
                encrypted_data = fernet.encrypt(file_data)
                file.close()
            # writes to the binary of a file
            with open(filepath, "wb") as file:
                file.write(encrypted_data)
                file.close()
            os.chdir(lockerdir)
            newfilename = (str(filename) + str('.ivf'))
            os.rename(fullfilename, newfilename)
            os.chdir(initialdir)
    except Exception as e:
        print("There was an error while adding this file")
        file = open('logs/error.log', 'a')
        errormsg = (str(e) + str('\n'))
        file.write(errormsg)
        file.close()
        finishedprocess()
        return
    print("File added successfully")


def deleteaccountcmd():
    rusure = input("Are you sure you want to delete your account? This will also purge your locker(y/n): ")
    if hmac.compare_digest(rusure, "y"):
        purgecmd(rusure=str("y"))
        delextensions = [".ivd", ".ivp"]
        for file_path in glob.glob(os.path.join(initialdir, "*")):
            if os.path.splitext(file_path)[1] in delextensions:
                os.remove(file_path)
        print("Account successfully deleted, closing in 10 seconds")
        time.sleep(10)
        exit()
    else:
        print("Cancelled")


def purgecmd(rusure):
    if hmac.compare_digest(rusure, "y"):
        for filename in os.listdir(lockerdir):
            file_path = os.path.join(lockerdir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                file = open('logs/error.log', 'a')
                errormsg = (str(e) + str('\n'))
                file.write(errormsg)
                file.close()
                print("There was an error while purging your locker")

        delextensions = [".ivd", ".ivs", ".ive"]
        for file_path in glob.glob(os.path.join(initialdir, "*")):
            if os.path.splitext(file_path)[1] in delextensions:
                os.remove(file_path)
        file = open('setupdone.ivd', 'w+')
        file.close()
        file = open('openfile.ivd', 'w+')
        file.write("NONE")
        file.close()
        print("Purge completed successfully")
    else:
        print("Cancelled")


def renamecmd():
    filepath = filedialog.askopenfilename(initialdir="./locker",
                                          title="Select a File",
                                          filetypes=(("all files",
                                                      "*.*"),
                                                     ("all files",
                                                      "*.*")))
    newname = input("What do you want to rename this file to: ")
    try:
        # find file extension
        file_extension = pathlib.Path(filepath).suffix
        renamepath = str(lockerdir) + str("/") + str(newname) + str(file_extension)
        os.rename(filepath, renamepath)
        filename = pathlib.Path(filepath).stem
        namefile = (str(filename) + str(".ive"))
        renamepath = str(initialdir) + str("/") + str(newname) + str(".ive")
        os.rename(namefile, renamepath)
        namefile = (str(filename) + str(".ivd"))
        renamepath = str(initialdir) + str("/") + str(newname) + str(".ivd")
        os.rename(namefile, renamepath)
        namefile = (str(filename) + str(".ivs"))
        renamepath = str(initialdir) + str("/") + str(newname) + str(".ivs")
        os.rename(namefile, renamepath)
        print("Successfully renamed file")
    except Exception as e:
        file = open('logs/error.log', 'a')
        errormsg = (str(e) + str('\n'))
        file.write(errormsg)
        file.close()
        print("Failed to rename file")


def setup():
    global password
    print("Doing first time setup")
    password = getpass.getpass(prompt='Enter password: ')
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
        closecmd()
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
        "add": addcmd,
        "open": opencmd,
        "close": closecmd,
        "help": helpcmd,
        "remove": removecmd,
        "list": listcmd,
        "rename": renamecmd,
        "delaccount": deleteaccountcmd,
    }

    for command, function in commands.items():
        if hmac.compare_digest(command, commandinput):
            function()
            return True

    return False


while True:
    commandinput = input(">> ").lower()
    if hmac.compare_digest(commandinput, "exit"):
        exitcmd()
        break
    elif hmac.compare_digest(commandinput, "purge"):
        rusure = input("Are you sure you want to purge your locker(y/n) ")
        purgecmd(rusure=rusure)
    elif not process_command(commandinput):
        print("Oops that's not a command \nUse help for a full list of commands")
