import os
import bcrypt
from tkinter import filedialog
import shutil
import pathlib
import base64
import hmac
import getpass
import lzma
from commands.security.hashfile import *
from commands.security.encryptions import *


def add_cmd(lockerdir, password, initialdir):
    filepath = filedialog.askopenfilename(initialdir="C:/",
                                          title="Select a File",
                                          filetypes=(("all files",
                                                      "*.*"),
                                                     ("all files",
                                                      "*.*")))
    if not filepath:
        return

    file_extension = pathlib.Path(filepath).suffix
    filename = pathlib.Path(filepath).stem
    full_filename = os.path.basename(filepath)
    shutil.move(filepath, "./locker")

    to_hash = str(str(lockerdir) + '/' + str(filename)).encode('utf-8')
    data_file_name = str(sha1_hash(to_hash=to_hash))

    newpass = input("Do you want to have a seperate password for this file(y/n): ")
    newpass = newpass.lower()

    enable_compression = input("Do you want to enable compression on this file(y/n): ")
    enable_compression = enable_compression.lower()

    if hmac.compare_digest(newpass, "y"):
        invalidinput = False
    elif hmac.compare_digest(newpass, "n"):
        invalidinput = False
    else:
        invalidinput = True

    if hmac.compare_digest(enable_compression, "y"):
        preset_lvl = input("Select compression level (1 = low, 9 = high, 6 = default): ")
        preset_lvl = int(preset_lvl)
        if preset_lvl < 1 or preset_lvl > 9:
            print("Invalid compression level, using default")
            preset_lvl = 6
        file_to_compress = str(str(lockerdir) + '/' + str(full_filename))
        print("Compressing - this may take some time")
        with open(file_to_compress, "rb") as input_file, lzma.open(file_to_compress + ".xz", "wb",
                                                                   preset=preset_lvl) as output_file:
            input_data = input_file.read()
            compressed_data = lzma.compress(input_data)
            output_file.write(compressed_data)
        os.remove(file_to_compress)

    if hmac.compare_digest(newpass, "y"):
        second_pass = "sp"
        salt = bcrypt.gensalt()

        # gets the user to input their password
        custompass = getpass.getpass(prompt='Enter password for this file: ')
        # adds password and salt together - then encodes
        passnsalt = (str(custompass) + str(salt))

        # hashes the password and salt to use as a key
        hashed = hashfile(to_hash=passnsalt)
        key = base64.urlsafe_b64encode(hashed)
        # gets new file path
        filepath = (str('./locker/') + str(full_filename) + ".xz")

        # Encrypt file
        with open(filepath, "rb") as file:
            file_data = file.read()
            encrypted_data = encryptfile(key=key, file_data=file_data)
            file.close()
        with open(filepath, "wb") as file:
            file.write(encrypted_data)
            file.close()

        originalpassnsalt = (str(password) + str(salt))
        # hashes the password and salt to use as a key
        hashed = hashfile(to_hash=originalpassnsalt)
        key = base64.urlsafe_b64encode(hashed)

        # Encrypt file
        with open(filepath, "rb") as file:
            file_data = file.read()
            encrypted_data = encryptfile(key=key, file_data=file_data)
            file.close()
        with open(filepath, "wb") as file:
            file.write(encrypted_data)
            file.close()

        os.chdir(lockerdir)
        newfilename = (str(filename) + str('.ivf'))
        os.rename(full_filename, newfilename)
        os.chdir(initialdir)
    else:
        if invalidinput:
            print("Invalid input - using default password")
        else:
            print("Using default password")

        second_pass = "nsp"
        salt = bcrypt.gensalt()

        # gets new file path
        filepath = (str('./locker/') + str(full_filename) + ".xz")
        originalpassnsalt = (str(password) + str(salt))

        # hashes the password and salt to use as a key
        hashed = hashfile(to_hash=originalpassnsalt)
        key = base64.urlsafe_b64encode(hashed)

        # Encrypt file
        with open(filepath, "rb") as file:
            file_data = file.read()
            encrypted_data = encryptfile(key=key, file_data=file_data)
            file.close()
        with open(filepath, "wb") as file:
            file.write(encrypted_data)
            file.close()

        os.chdir(lockerdir)
        newfilename = (str(filename) + str('.ivf'))
        os.rename(full_filename + ".xz", newfilename)
        os.chdir(initialdir)

    data_file_path = str(str(initialdir) + '/data/' + data_file_name + '.data')
    with open(data_file_path, 'w+') as data_file:
        file_content = str(str(file_extension)
                           + ','
                           + str(salt)
                           + ','
                           + str(second_pass)
                           + ','
                           + str(enable_compression))
        data_file.write(file_content)

    print("File added successfully")
    return
