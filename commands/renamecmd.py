import os
from tkinter import filedialog
import pathlib
from commands.security.hashfile import sha1_hash


def renamecmd(lockerdir, initialdir):
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

        to_hash = str(str(lockerdir) + '/' + str(filename)).encode('utf-8')
        data_file_name = str(sha1_hash(to_hash=to_hash))
        old_data_file_path = str(str(initialdir) + '/data/' + data_file_name + '.data')
        to_hash = str(str(lockerdir) + '/' + str(newname)).encode('utf-8')
        data_file_name = str(sha1_hash(to_hash=to_hash))
        new_data_file_path = str(str(initialdir) + '/data/' + data_file_name + '.data')
        os.rename(old_data_file_path, new_data_file_path)

        print("Successfully renamed file")
    except Exception as e:
        file = open('logs/error.log', 'a')
        errormsg = (str(e) + str('\n'))
        file.write(errormsg)
        file.close()
        print("Failed to rename file")
