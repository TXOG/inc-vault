import os
import pathlib
import base64
import hmac
import getpass
import lzma
from iscript.error.finishedprocess import finishedprocess
from iscript.security.hash import *
from iscript.security.encryption import *


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
        enable_compression = file_data[3]
        hash_salt = file_data[4]

    if hmac.compare_digest(enable_compression, "y"):
        preset_lvl = input("Which compression level would you like to use: ")
        preset_lvl = int(preset_lvl)
        if preset_lvl < 1 or preset_lvl > 9:
            print("Invalid compression level, using default")
            preset_lvl = 6
        file_to_compress = str(str(lockerdir) + '/' + str(fullfilename))
        print("Compressing - this may take some time")
        with open(file_to_compress, "rb") as input_file, lzma.open(file_to_compress + ".xz", "wb",
                                                                   preset=preset_lvl) as output_file:
            input_data = input_file.read()
            compressed_data = lzma.compress(input_data)
            output_file.write(compressed_data)
        os.remove(file_to_compress)

        encrypt_filepath = str(filename) + str(extension) + ".xz"
    else:
        encrypt_filepath = fullfilename

    if hmac.compare_digest(second_pass, "sp"):
        custompass = getpass.getpass(prompt='Enter a new password for this file: ')
        # adds password and salt together - then encodes
        passnsalt = (str(custompass) + str(salt))
        # hashes the password and salt to use as a key
        hashed = hashfile(to_hash=passnsalt, hash_salt=hash_salt)
        key = base64.urlsafe_b64encode(hashed)
        os.chdir(lockerdir)

        # Encrypt file
        with open(encrypt_filepath, "rb") as file:
            file_data = file.read()
            encrypted_data = encryptfile(key=key, file_data=file_data)
            file.close()
        with open(encrypt_filepath, "wb") as file:
            file.write(encrypted_data)
            file.close()

        os.chdir(initialdir)
        originalpassnsalt = (str(password) + str(salt))
        # hashes the password and salt to use as a key
        hashed = hashfile(to_hash=originalpassnsalt, hash_salt=hash_salt)
        key = base64.urlsafe_b64encode(hashed)
        os.chdir(lockerdir)

        # Encrypt file
        with open(encrypt_filepath, "rb") as file:
            file_data = file.read()
            encrypted_data = encryptfile(key=key, file_data=file_data)
            file.close()
        with open(encrypt_filepath, "wb") as file:
            file.write(encrypted_data)
            file.close()

        newfilename = (str(filename) + str('.ivf'))
        if hmac.compare_digest(enable_compression, "y"):
            os.rename(str(filename) + str(extension) + ".xz", newfilename)
        else:
            os.rename(fullfilename, newfilename)
        os.chdir(initialdir)
    else:
        originalpassnsalt = (str(password) + str(salt))
        # hashes the password and salt to use as a key
        hashed = hashfile(to_hash=originalpassnsalt, hash_salt=hash_salt)
        key = base64.urlsafe_b64encode(hashed)
        os.chdir(lockerdir)

        # Encrypt file
        with open(encrypt_filepath, "rb") as file:
            file_data = file.read()
            encrypted_data = encryptfile(key=key, file_data=file_data)
            file.close()
        with open(encrypt_filepath, "wb") as file:
            file.write(encrypted_data)
            file.close()

        newfilename = (str(filename) + str('.ivf'))
        if hmac.compare_digest(enable_compression, "y"):
            os.rename(str(filename) + str(extension) + ".xz", newfilename)
        else:
            os.rename(fullfilename, newfilename)
        os.chdir(initialdir)
    file = open('openfile.ivd', 'w+')
    file.truncate(0)
    file.write("NONE")
    file.close()
    print("File closed successfully")
    return
