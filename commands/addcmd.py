import os
import bcrypt
from tkinter import filedialog
import shutil
import pathlib
import base64
import hmac
import getpass
from commands.security.hashfile import hashfile
from commands.security.encryptions import *
from commands.error.finishedprocess import finishedprocess


def addcmd(password, lockerdir, initialdir):
    try:
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
            # gets new file path
            filepath = (str('./locker/') + str(filename) + str(file_extension))
            # gets the bytes data of a file and encrypts
            with open(filepath, "rb") as file:
                file_data = file.read()
                encrypted_data = encryptfile(key=key, file_data=file_data)
                file.close()
            # writes to the binary of a file
            with open(filepath, "wb") as file:
                file.write(encrypted_data)
                file.close()
            originalpassnsalt = (str(password) + str(salt))
            # hashes the password and salt to use as a key
            hashed = hashfile(to_hash=originalpassnsalt)
            key = base64.urlsafe_b64encode(hashed)
            # gets the bytes data of a file and encrypts
            with open(filepath, "rb") as file:
                file_data = file.read()
                encrypted_data = encryptfile(key=key, file_data=file_data)
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
            # gets the bytes data of a file and encrypts
            with open(filepath, "rb") as file:
                file_data = file.read()
                encrypted_data = encryptfile(key=key, file_data=file_data)
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
    return
