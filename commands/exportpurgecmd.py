import os
import shutil


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
