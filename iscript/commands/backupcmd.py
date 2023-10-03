import os
import shutil
import zipfile


def backup(lockerdir, initialdir):
    if os.path.exists('backup.zip'):
        os.remove('backup.zip')

    if not os.path.exists('./backup'):
        os.mkdir('./backup')

    shutil.copytree(lockerdir, './backup/locker')
    shutil.copytree((str(initialdir) + '/data'), './backup/data')

    extensions = (".ivd", ".ivp", ".ive", ".ivs")
    for filename in os.listdir(".."):
        if filename.endswith(extensions):
            source_path = os.path.join("..", filename)
            destination_path = os.path.join('./backup/', filename)
            shutil.copy(source_path, destination_path)

    with zipfile.ZipFile('backup.zip', "w", compression=zipfile.ZIP_LZMA) as zip_obj:
        for foldername, subfolders, filenames in os.walk('./backup'):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zip_obj.write(file_path)

    shutil.rmtree('./backup')

    print("backup.zip created in IncVault folder")
