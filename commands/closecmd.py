import os
import pathlib
import base64
import hmac
import getpass
from commands.error.finishedprocess import finishedprocess
from commands.security.hashfile import *
from commands.security.encryptions import *


def close_cmd(password, lockerdir, initialdir):
    file = open('openfile.ivd', 'r+')
    mostrecentpath = file.read().strip()
    file.close()

    if hmac.compare_digest(mostrecentpath, "NONE"):
        print("All files are closed")
        finishedprocess()
        return

    filename = pathlib.Path(mostrecentpath).stem
    fullfilename = os.path.basename(mostrecentpath).strip()

    to_hash = str(str(lockerdir) + '/' + str(filename)).encode('utf-8')
    data_file_name = str(sha1_hash(to_hash=to_hash))
    data_file_path = str(str(initialdir) + '/data/' + data_file_name + '.data')

    with open(data_file_path, 'r') as data_file:
        file_data = data_file.read()
        file_data = file_data.split(',')
        extension = file_data[0]
        salt = file_data[1]
        second_pass = file_data[2]

    if hmac.compare_digest(second_pass, "sp"):
        custompass = getpass.getpass(prompt='Enter password a new password for this file: ')
        # adds password and salt together - then encodes
        passnsalt = (str(custompass) + str(salt))
        # hashes the password and salt to use as a key
        hashed = hashfile(to_hash=passnsalt)
        key = base64.urlsafe_b64encode(hashed)
        os.chdir(lockerdir)

        # Encrypt file
        with open(fullfilename, "rb") as file:
            file_data = file.read()
            encrypted_data = encryptfile(key=key, file_data=file_data)
            file.close()
        with open(fullfilename, "wb") as file:
            file.write(encrypted_data)
            file.close()

        os.chdir(initialdir)
        originalpassnsalt = (str(password) + str(salt))
        # hashes the password and salt to use as a key
        hashed = hashfile(to_hash=originalpassnsalt)
        key = base64.urlsafe_b64encode(hashed)
        os.chdir(lockerdir)

        # Encrypt file
        with open(fullfilename, "rb") as file:
            file_data = file.read()
            encrypted_data = encryptfile(key=key, file_data=file_data)
            file.close()
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
        os.chdir(lockerdir)

        # Encrypt file
        with open(fullfilename, "rb") as file:
            file_data = file.read()
            encrypted_data = encryptfile(key=key, file_data=file_data)
            file.close()
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
    return

