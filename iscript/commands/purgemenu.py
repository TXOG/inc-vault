import os
import shutil
import hmac
from iscript.commands.closecmd import close_cmd


def purgemenu(lockerdir, initialdir, initialinput, password):
    splitcommand = initialinput.split()
    try:
        if hmac.compare_digest(splitcommand[1], "help"):
            print("Here's a list of purge options: "
                  "\n To purge your locker use: purge -l"
                  "\n To purge your export folder use: purge -e"
                  )
        elif hmac.compare_digest(splitcommand[1], "-l"):
            rusure = input("Are you sure you want to purge your locker(y/n) ")
            purgecmd(rusure=rusure, lockerdir=lockerdir, initialdir=initialdir, password=password)
        elif hmac.compare_digest(splitcommand[1], "-e"):
            purgeexportcmd(initialdir=initialdir)
        else:
            print('Invalid purge option, try "purge help"')
    except:
        print('Invalid purge option, try "purge help"')
    return


def purgeexportcmd(initialdir):
    purge_folder = str(initialdir) + str('/export/')
    for filename in os.listdir(purge_folder):
        file_path = os.path.join(purge_folder, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    print("Purge completed successfully")
    return


def purgecmd(rusure, lockerdir, initialdir, password):
    if hmac.compare_digest(rusure, "y"):
        close_cmd(password=password, lockerdir=lockerdir, initialdir=initialdir)
        try:
            for filename in os.listdir(lockerdir):
                file_path = os.path.join(lockerdir, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)

            for filename in os.listdir(str(initialdir) + '/data/'):
                file_path = os.path.join(str(initialdir) + '/data/', filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        except Exception as e:
            file = open('logs/error.log', 'a')
            errormsg = (str(e) + str('\n'))
            file.write(errormsg)
            file.close()
            print("There was an error while purging your locker")
            return

        print("Purge completed successfully")
    else:
        print("Cancelled")
    return
