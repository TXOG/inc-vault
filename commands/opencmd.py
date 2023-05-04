import os
from tkinter import filedialog
import shutil
import pathlib
import base64
import hmac
import getpass
from commands.error.finishedprocess import finishedprocess
from commands.security.hashfile import hashfile
from commands.security.encryptions import *


def opencmd(password, lockerdir, initialdir, prevcmd):
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
                with open(filepath, "rb") as file:
                    file_data = file.read()
                    decrypted_data = decryptfile(key=key, file_data=file_data)
                    file.close()
                # writes to the binary of a file
                with open(filepath, "wb") as file:
                    file.write(decrypted_data)
                    file.close()
                # decrypting with new differnet password
                cpassnsalt = (str(custompass) + str(salt))
                hash = hashfile(to_hash=cpassnsalt)
                key = base64.urlsafe_b64encode(hash)
                with open(filepath, "rb") as file:
                    file_data = file.read()
                    decrypted_data = decryptfile(key=key, file_data=file_data)
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
                with open(filepath, "rb") as file:
                    file_data = file.read()
                    decrypted_data = decryptfile(key=key, file_data=file_data)
                    file.close()
                # writes to the binary of a file
                with open(filepath, "wb") as file:
                    file.write(decrypted_data)
                    file.close()
                revertfilename = (str(filename) + str(extension))
                os.chdir(lockerdir)
                os.rename(filepath, revertfilename)
                os.chdir(initialdir)
                # open in default application
                path2open = (str(lockerdir) + str('/')
                             + str(filename) + str(extension))
                if not prevcmd == "export":
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
    if prevcmd == "export":
        return revertfilename
