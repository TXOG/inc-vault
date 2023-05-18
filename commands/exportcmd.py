import os
import shutil
from commands.opencmd import open_cmd
from commands.closecmd import close_cmd
from commands.error.finishedprocess import finishedprocess


def exportcmd(password, initialdir, lockerdir):
    filename = open_cmd(password=password, lockerdir=lockerdir, initialdir=initialdir, prevcmd="export")
    try:
        source_file = os.path.join(lockerdir, filename)
        destination_dir = os.path.join(initialdir, 'export')
        shutil.copy(source_file, destination_dir)
        close_cmd(password=password, lockerdir=lockerdir, initialdir=initialdir)
        print("File successfully exported")
    except:
        print("Looks like that file already exists in your export folder")
        close_cmd(password=password, lockerdir=lockerdir, initialdir=initialdir)
        finishedprocess()
