import os
from tkinter import filedialog
import pathlib


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
        namefile = (str(filename) + str(".ive"))
        renamepath = str(initialdir) + str("/") + str(newname) + str(".ive")
        os.rename(namefile, renamepath)
        namefile = (str(filename) + str(".ivd"))
        renamepath = str(initialdir) + str("/") + str(newname) + str(".ivd")
        os.rename(namefile, renamepath)
        namefile = (str(filename) + str(".ivs"))
        renamepath = str(initialdir) + str("/") + str(newname) + str(".ivs")
        os.rename(namefile, renamepath)
        print("Successfully renamed file")
    except Exception as e:
        file = open('logs/error.log', 'a')
        errormsg = (str(e) + str('\n'))
        file.write(errormsg)
        file.close()
        print("Failed to rename file")
