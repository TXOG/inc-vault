import os
import shutil
import zipfile


def backup(lockerdir, initialdir):
    print("This command currently does not work fully, and has therefore been disabled for now. Please try again in the next update. \nCopy and paste the whole IncVault directory now if you wish to create a backup")
    # if os.path.exists('backup.zip'):
    #     os.remove('backup.zip')
    #
    # if not os.path.exists('./backup'):
    #     os.mkdir('./backup')
    #
    # shutil.copytree(lockerdir, './backup/locker')
    # shutil.copytree((str(initialdir) + '/data'), './backup/data')
    #
    # extensions = (".ivd", ".ivp", ".ive", ".ivs")
    # for filename in os.listdir(".."):
    #     if filename.endswith(extensions):
    #         source_path = os.path.join("..", filename)
    #         destination_path = os.path.join('./backup/', filename)
    #         shutil.copy(source_path, destination_path)
    #         print("Added " + str(filename) + " to backup zip")
    #
    # with zipfile.ZipFile('backup.zip', "w", compression=zipfile.ZIP_LZMA) as zip_obj:
    #     for foldername, subfolders, filenames in os.walk('./backup'):
    #         for filename in filenames:
    #             file_path = os.path.join(foldername, filename)
    #             zip_obj.write(file_path)
    #
    # shutil.rmtree('./backup')
    #
    # print("backup.zip created in IncVault folder")
