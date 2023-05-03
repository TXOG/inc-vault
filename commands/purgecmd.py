import os
import shutil
import glob
import hmac


def purgecmd(rusure, lockerdir, initialdir):
    if hmac.compare_digest(rusure, "y"):
        for filename in os.listdir(lockerdir):
            file_path = os.path.join(lockerdir, filename)
            try:
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

        delextensions = [".ivd", ".ivs", ".ive"]
        for file_path in glob.glob(os.path.join(initialdir, "*")):
            if os.path.splitext(file_path)[1] in delextensions:
                os.remove(file_path)
        file = open('setupdone.ivd', 'w+')
        file.close()
        file = open('openfile.ivd', 'w+')
        file.write("NONE")
        file.close()
        print("Purge completed successfully")
    else:
        print("Cancelled")