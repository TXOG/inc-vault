import os
import time
import glob
import hmac
from iscript.commands.purgemenu import purgecmd


def deleteaccountcmd(initialdir, lockerdir, password):
    rusure = input("Are you sure you want to delete your account? This will also purge your locker(y/n): ")
    if hmac.compare_digest(rusure, "y"):
        purgecmd(rusure=str("y"), lockerdir=lockerdir, initialdir=initialdir, password=password)
        delextensions = [".ivd", ".ivp"]
        for file_path in glob.glob(os.path.join(initialdir, "*")):
            if os.path.splitext(file_path)[1] in delextensions:
                os.remove(file_path)
        print("Account successfully deleted, closing in 10 seconds")
        time.sleep(10)
        exit()
    else:
        print("Cancelled")