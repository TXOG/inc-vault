import os
from tkinter import filedialog
import pathlib
import hmac
from iscript.commands.closecmd import close_cmd
from iscript.security.hash import sha1_hash


def removecmd(password, lockerdir, initialdir):
    close_cmd(password=password, lockerdir=lockerdir, initialdir=initialdir)
    couldntremove = "NONE"
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
            os.remove(filepath)

            to_hash = str(str(lockerdir) + '/' + str(filename)).encode('utf-8')
            data_file_name = str(sha1_hash(to_hash=to_hash))
            data_file_path = str(str(initialdir) + '/data/' + data_file_name + '.data')

            os.remove(data_file_path)

            print("Successfully removed file")
        except Exception as e:
            print("There was an error removing file")
            file = open('logs/error.log', 'a')
            errormsg = (str(e) + str('\n'))
            file.write(errormsg)
            file.close()
    else:
        print("Cancelled")
