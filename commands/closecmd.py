import os
import pathlib
import base64
import hmac
import getpass
from commands.error.finishedprocess import finishedprocess
from commands.security.hashfile import hashfile
from commands.security.encryptions import *


def closecmd(password, lockerdir, initialdir):
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
                # gets new file path
                # gets the bytes data of a file and encrypts
                os.chdir(lockerdir)
                with open(fullfilename, "rb") as file:
                    file_data = file.read()
                    encrypted_data = encryptfile(key=key, file_data=file_data)
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
                # gets the bytes data of a file and encrypts
                os.chdir(lockerdir)
                with open(fullfilename, "rb") as file:
                    file_data = file.read()
                    encrypted_data = encryptfile(key=key, file_data=file_data)
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
                # gets the bytes data of a file and encrypts
                os.chdir(lockerdir)
                with open(fullfilename, "rb") as file:
                    file_data = file.read()
                    encrypted_data = encryptfile(key=key, file_data=file_data)
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
