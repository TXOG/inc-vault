import os
from tkinter import filedialog
import shutil
import pathlib
import base64
import hmac
import getpass
import lzma
from commands.error.finishedprocess import finishedprocess
from commands.security.hashfile import *
from commands.security.encryptions import *


def open_cmd(password, lockerdir, initialdir, prevcmd):
    # Check if file already opened
    file = open('openfile.ivd', 'r+')
    mostrecentpath = file.read().strip()
    file.close()

    if not hmac.compare_digest(mostrecentpath, "NONE"):
        print("Please close the last file you opened with the command: close")
        finishedprocess()
        return

    split_command = prevcmd.split()

    filepath = filedialog.askopenfilename(initialdir="./locker",
                                          title="Select a File",
                                          filetypes=(("IVF files", "*.ivf"),))

    filename = pathlib.Path(filepath).stem
    fullfilename = os.path.basename(filepath)

    to_hash = str(str(lockerdir) + '/' + str(filename)).encode('utf-8')
    data_file_name = str(sha1_hash(to_hash=to_hash))
    data_file_path = str(str(initialdir) + '/data/' + data_file_name + '.data')

    with open(data_file_path, 'r') as data_file:
        file_data = data_file.read()
        file_data = file_data.split(',')
        extension = file_data[0]
        salt = file_data[1]
        second_pass = file_data[2]
        enable_compression = file_data[3]
        hash_salt = file_data[4]

        if hmac.compare_digest(second_pass, "sp"):
            shutil.copy(filepath, initialdir)
            backuppath = (str(initialdir) + str('/') + str(fullfilename))
            backupfullfilename = os.path.basename(backuppath)

            try:
                # getting custom password
                custompass = getpass.getpass(prompt='Enter password: ')

                passnsalt = (str(password) + str(salt))
                hash = hashfile(to_hash=passnsalt, hash_salt=hash_salt)
                key = base64.urlsafe_b64encode(hash)

                # Decrypting file
                with open(filepath, "rb") as file:
                    file_data = file.read()
                    decrypted_data = decryptfile(key=key, file_data=file_data)
                    file.close()
                with open(filepath, "wb") as file:
                    file.write(decrypted_data)
                    file.close()

                cpassnsalt = (str(custompass) + str(salt))
                hash = hashfile(to_hash=cpassnsalt, hash_salt=hash_salt)
                key = base64.urlsafe_b64encode(hash)

                # Decrypting file
                with open(filepath, "rb") as file:
                    file_data = file.read()
                    decrypted_data = decryptfile(key=key, file_data=file_data)
                    file.close()
                with open(filepath, "wb") as file:
                    file.write(decrypted_data)
                    file.close()

                # rename the file
                if hmac.compare_digest(enable_compression, "y"):
                    revertfilename = (str(filename) + str(extension) + ".xz")
                else:
                    revertfilename = str(filename) + str(extension)
                os.chdir(lockerdir)
                os.rename(filepath, revertfilename)

                if hmac.compare_digest(enable_compression, "y"):
                    with lzma.open(str(lockerdir) + '/' + revertfilename, "rb") as input_file,\
                            open(str(lockerdir) + '/' + str(filename) + str(extension), "wb") as output_file:
                        compressed_data = input_file.read()
                        decompressed_data = lzma.decompress(compressed_data)
                        output_file.write(decompressed_data)
                    os.remove(str(lockerdir) + '/' + str(filename) + str(extension) + ".xz")
                os.chdir(initialdir)

                # open in default application
                path2open = (str(lockerdir) + str('/') + str(filename) + str(extension))
                os.remove(backupfullfilename)
                try:
                    if not hmac.compare_digest(split_command[1], "-n"):
                        if not prevcmd == "export":
                            os.startfile(path2open)

                except:
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
                passnsalt = (str(password) + str(salt))
                hash = hashfile(to_hash=passnsalt, hash_salt=hash_salt)
                key = base64.urlsafe_b64encode(hash)

                # Decrypting file
                with open(filepath, "rb") as file:
                    file_data = file.read()
                    decrypted_data = decryptfile(key=key, file_data=file_data)
                    file.close()
                with open(filepath, "wb") as file:
                    file.write(decrypted_data)
                    file.close()
                if hmac.compare_digest(enable_compression, "y"):
                    revertfilename = (str(filename) + str(extension) + ".xz")
                else:
                    revertfilename = str(filename) + str(extension)
                os.chdir(lockerdir)
                os.rename(filepath, revertfilename)
                if hmac.compare_digest(enable_compression, "y"):
                    with lzma.open(str(lockerdir) + '/' + revertfilename, "rb") as input_file, \
                            open(str(lockerdir) + '/' + str(filename) + str(extension), "wb") as output_file:
                        compressed_data = input_file.read()
                        decompressed_data = lzma.decompress(compressed_data)
                        output_file.write(decompressed_data)
                    os.remove(str(lockerdir) + '/' + str(filename) + str(extension) + ".xz")
                os.chdir(initialdir)

                # open in default application
                path2open = (str(lockerdir) + str('/') + str(filename) + str(extension))
                try:
                    if not hmac.compare_digest(split_command[1], "-n"):
                        if not prevcmd == "export":
                            os.startfile(path2open)

                except:
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
