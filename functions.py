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


def helpcmd():
    print("Here's a list of all commands that are avaliable at the moment: \n \nadd: Use this by istelf, adds a file to the system \nclose: Use this by itself, closes the last file opened (don't forget to do this before exiting) \nexit: Use this by itself, exits the program \nhelp: Shows this message :) \nopen: Use this by itself, opens a file selected from a gui")


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

        if mostrecentpath == ("NONE"):
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

            if data == ("sp"):
                #gets the user to input their password
                custompass = input(
                    "Enter password for this file (This passowrd can be different to the one set previously): ")
                #adds password and salt together - then encodes
                passnsalt = (str(custompass) + str(salt))
                passnsalt = passnsalt.encode('utf-8')
                #hashes the password and salt to use as a key
                hashed = hashlib.sha256(passnsalt).digest()
                key = base64.urlsafe_b64encode(hashed)
                #creates fernet so encryption can happen
                fernet = Fernet(key)
                #gets new file path
                #gets the bytes data of a file and encrypts
                os.chdir(lockerdir)
                with open(fullfilename, "rb") as file:
                    file_data = file.read()
                    encrypted_data = fernet.encrypt(file_data)
                    file.close()
                #writes to the binary of a file
                with open(fullfilename, "wb") as file:
                    file.write(encrypted_data)
                    file.close()
                os.chdir(initialdir)
                originalpassnsalt = (str(password) + str(salt))
                originalpassnsalt = originalpassnsalt.encode('utf-8')
                #hashes the password and salt to use as a key
                hashed = hashlib.sha256(originalpassnsalt).digest()
                key = base64.urlsafe_b64encode(hashed)
                #creates fernet so encryption can happen
                fernet = Fernet(key)
                #gets the bytes data of a file and encrypts
                os.chdir(lockerdir)
                with open(fullfilename, "rb") as file:
                    file_data = file.read()
                    encrypted_data = fernet.encrypt(file_data)
                    file.close()
                #writes to the binary of a file
                with open(fullfilename, "wb") as file:
                    file.write(encrypted_data)
                    file.close()
                newfilename = (str(filename) + str('.ivf'))
                os.rename(fullfilename, newfilename)
                os.chdir(initialdir)
            else:
                originalpassnsalt = (str(password) + str(salt))
                originalpassnsalt = originalpassnsalt.encode('utf-8')
                #hashes the password and salt to use as a key
                hashed = hashlib.sha256(originalpassnsalt).digest()
                key = base64.urlsafe_b64encode(hashed)
                #creates fernet so encryption can happen
                fernet = Fernet(key)
                #gets the bytes data of a file and encrypts
                os.chdir(lockerdir)
                with open(fullfilename, "rb") as file:
                    file_data = file.read()
                    encrypted_data = fernet.encrypt(file_data)
                    file.close()
                #writes to the binary of a file
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

    except:
        print("There was an error while trying to close this file")
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

    if mostrecentpath != ("NONE"):
        print("Please close the last file you opened with the command: close")
        finishedprocess()
    else:

        filepath = filedialog.askopenfilename(initialdir="./locker",
                                              title="Select a File",
                                              filetypes=(("all files",
                                                          "*.*"),
                                                         ("all files",
                                                          "*.*")))
        #find filename without extension
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
        except:
            print("One or more files don't exist, to open you must restore them")
            finishedprocess()
            return

        #Seeing if there is a seperate password
        if data == ("sp"):
            shutil.copy(filepath, initialdir)
            backuppath = (str(initialdir) + str('/') + str(fullfilename))
            backupfullfilename = os.path.basename(backuppath)
            try:
                #getting custom password
                custompass = input("Enter password: ")
                #decrypting with orignial password first
                passnsalt = (str(password) + str(salt))
                passnsalt = passnsalt.encode('utf-8')
                hash = hashlib.sha256(passnsalt).digest()
                key = base64.urlsafe_b64encode(hash)
                fernet = Fernet(key)
                with open(filepath, "rb") as file:
                    file_data = file.read()
                    decrypted_data = fernet.decrypt(file_data)
                    file.close()
                #writes to the binary of a file
                with open(filepath, "wb") as file:
                    file.write(decrypted_data)
                    file.close()
                #decrypting with new differnet password
                cpassnsalt = (str(custompass) + str(salt))
                cpassnsalt = cpassnsalt.encode('utf-8')
                hash = hashlib.sha256(cpassnsalt).digest()
                key = base64.urlsafe_b64encode(hash)
                fernet = Fernet(key)
                with open(filepath, "rb") as file:
                    file_data = file.read()
                    decrypted_data = fernet.decrypt(file_data)
                    file.close()
                #writes to the binary of a file
                with open(filepath, "wb") as file:
                    file.write(decrypted_data)
                    file.close()
                #rename the file
                revertfilename = (str(filename) + str(extension))
                os.chdir(lockerdir)
                os.rename(filepath, revertfilename)
                os.chdir(initialdir)
                #open in defualt application
                path2open = (str(lockerdir) + str('/')
                             + str(filename) + str(extension))
                os.remove(backupfullfilename)
                os.startfile(path2open)
            except:
                print(
                    "There was an error while opening this file, maybe you used the wrong password?")
                os.chdir(lockerdir)
                os.remove(backupfullfilename)
                os.chdir(initialdir)
                shutil.copy(backuppath, lockerdir)
                os.remove(backupfullfilename)
                finishedprocess()
                return
        else:
            try:
                #decrypting with orignial password
                passnsalt = (str(password) + str(salt))
                passnsalt = passnsalt.encode('utf-8')
                hash = hashlib.sha256(passnsalt).digest()
                key = base64.urlsafe_b64encode(hash)
                fernet = Fernet(key)
                with open(filepath, "rb") as file:
                    file_data = file.read()
                    decrypted_data = fernet.decrypt(file_data)
                    file.close()
                #writes to the binary of a file
                with open(filepath, "wb") as file:
                    file.write(decrypted_data)
                    file.close()
                revertfilename = (str(filename) + str(extension))
                os.chdir(lockerdir)
                os.rename(filepath, revertfilename)
                os.chdir(initialdir)
                #open in defualt application
                path2open = (str(lockerdir) + str('/')
                             + str(filename) + str(extension))
                os.startfile(path2open)
            except:
                print("There was error while trying to open the file")
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
        #gui to choose files
        filepath = filedialog.askopenfilename(initialdir="./locker",
                                              title="Select a File",
                                              filetypes=(("all files",
                                                          "*.*"),
                                                         ("all files",
                                                          "*.*")))
        #find file extension
        file_extension = pathlib.Path(filepath).suffix
        #find filename without extension
        filename = pathlib.Path(filepath).stem
        #find file name with extenion
        fullfilename = os.path.basename(filepath)
        #writes file extension to file
        namefile = (str(filename) + str('.ive'))
        file = open(namefile, 'w+')
        file.write(file_extension)
        file.close()
        #moves file to locker folder
        shutil.move(filepath, "./locker")
        #allows user to choose if custom password for this specific file
        newpass = input(
            "Do you want to have a seperate password for this file(y/n): ")
        newpass.lower()
        if newpass == ("y"):
            invalidinput = False
        elif newpass == ("n"):
            invalidinput = False
        else:
            invalidinput = True
        if newpass == ("y"):
            #writes to a file that seperate password
            namefile = (str(filename) + str('.ivd'))
            file = open(namefile, 'w+')
            file.write("sp")
            file.close()
            #generates a random salt
            salt = bcrypt.gensalt()
            #gets the user to input their password
            custompass = input("Enter password for this file: ")
            #adds password and salt together - then encodes
            passnsalt = (str(custompass) + str(salt))
            passnsalt = passnsalt.encode('utf-8')
            #writes the salt to a file
            namefile = (str(filename) + str('.ivs'))
            file = open(namefile, 'w+')
            file.write(str(salt))
            file.close()
            #hashes the password and salt to use as a key
            hashed = hashlib.sha256(passnsalt).digest()
            key = base64.urlsafe_b64encode(hashed)
            #creates fernet so encryption can happen
            fernet = Fernet(key)
            #gets new file path
            filepath = (str('./locker/') + str(filename) + str(file_extension))
            #gets the bytes data of a file and encrypts
            with open(filepath, "rb") as file:
                file_data = file.read()
                encrypted_data = fernet.encrypt(file_data)
                file.close()
            #writes to the binary of a file
            with open(filepath, "wb") as file:
                file.write(encrypted_data)
                file.close()
            originalpassnsalt = (str(password) + str(salt))
            originalpassnsalt = originalpassnsalt.encode('utf-8')
            #hashes the password and salt to use as a key
            hashed = hashlib.sha256(originalpassnsalt).digest()
            key = base64.urlsafe_b64encode(hashed)
            #creates fernet so encryption can happen
            fernet = Fernet(key)
            #gets the bytes data of a file and encrypts
            with open(filepath, "rb") as file:
                file_data = file.read()
                encrypted_data = fernet.encrypt(file_data)
                file.close()
            #writes to the binary of a file
            with open(filepath, "wb") as file:
                file.write(encrypted_data)
                file.close()
            os.chdir(lockerdir)
            newfilename = (str(filename) + str('.ivf'))
            os.rename(fullfilename, newfilename)
            os.chdir(initialdir)
        else:
            if invalidinput == True:
                print("Invalid input - using default password")
            else:
                print("Using default password")
            #writes to a file that same password
            namefile = (str(filename) + str('.ivd'))
            file = open(namefile, 'w+')
            file.write("nsp")
            file.close()
            #generates a random salt
            salt = bcrypt.gensalt()
            #writes the salt to a file
            namefile = (str(filename) + str('.ivs'))
            file = open(namefile, 'w+')
            file.write(str(salt))
            file.close()
            #gets new file path
            filepath = (str('./locker/') + str(filename) + str(file_extension))
            originalpassnsalt = (str(password) + str(salt))
            originalpassnsalt = originalpassnsalt.encode('utf-8')
            #hashes the password and salt to use as a key
            hashed = hashlib.sha256(originalpassnsalt).digest()
            key = base64.urlsafe_b64encode(hashed)
            #creates fernet so encryption can happen
            fernet = Fernet(key)
            #gets the bytes data of a file and encrypts
            with open(filepath, "rb") as file:
                file_data = file.read()
                encrypted_data = fernet.encrypt(file_data)
                file.close()
            #writes to the binary of a file
            with open(filepath, "wb") as file:
                file.write(encrypted_data)
                file.close()
            os.chdir(lockerdir)
            newfilename = (str(filename) + str('.ivf'))
            os.rename(fullfilename, newfilename)
            os.chdir(initialdir)
    except:
        print("There was an error while adding this file")
        finishedprocess()
        return
    print("File added successfully")


def setup():
    global password
    print("Doing first time setup")
    password = input("Enter password: ")
    password = password.encode('utf-8')
    hashed = hashlib.sha512(password).digest()
    #hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    file = open('password.ivp', 'w+')
    writehashed = str(hashed)
    file.write(writehashed)
    file.close()
    newpath = r'./locker'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    file = open('setupdone.ivd', 'w+')
    file.close()
    os.system('cls||clear')


def check_setup():
    global password
    if exists('setupdone.ivd'):
        global passnotcorrect
        passnotcorrect = True
        while passnotcorrect == True:
            password = input("Enter password: ")
            password = password.encode('utf-8')
            file = open('password.ivp', 'r')
            checkhash = file.read()
            file.close()
            #checkhash = checkhash.encode('utf-8')
            passwordcheck = hashlib.sha512(password).digest()
            if str(passwordcheck) == str(checkhash):
                passnotcorrect = False
                os.system('cls||clear')
            #if bcrypt.checkpw(password, checkhash):
            #    passnotcorrect = False
            #    os.system('cls||clear')
            else:
                print("Password is incorrect \n")

    else:
        setup()
