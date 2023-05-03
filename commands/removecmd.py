import os
from tkinter import filedialog
import pathlib
import hmac
from commands.closecmd import closecmd


def removecmd(password, lockerdir, initialdir):
    closecmd(password=password, lockerdir=lockerdir, initialdir=initialdir)
    couldntremove = ("NONE")
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
            couldntremove = (filename)
            os.remove(filepath)
            namefile = (str(filename) + str(".ive"))
            couldntremove = (namefile)
            os.remove(namefile)
            namefile = (str(filename) + str(".ivd"))
            couldntremove = (namefile)
            os.remove(namefile)
            namefile = (str(filename) + str(".ivs"))
            couldntremove = (namefile)
            os.remove(namefile)
            print("Successfully removed file")
        except Exception as e:
            print("There was an error removing file")
            print("Couldn't remove:")
            print(couldntremove)
            file = open('logs/error.log', 'a')
            errormsg = (str(e) + str('\n'))
            file.write(errormsg)
            file.close()
    else:
        print("Cancelled")
