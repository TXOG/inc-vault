import os
from tkinter import filedialog
import pathlib
from datetime import datetime
from iscript.security.hash import sha1_hash


def infocmd(lockerdir, initialdir):
    filepath = filedialog.askopenfilename(initialdir="./locker",
                                          title="Select a File",
                                          filetypes=(("all files",
                                                      "*.*"),
                                                     ("all files",
                                                      "*.*")))
    filename = pathlib.Path(filepath).stem

    to_hash = str(str(lockerdir) + '/' + str(filename)).encode('utf-8')
    data_file_name = str(sha1_hash(to_hash=to_hash))
    data_file_path = str(str(initialdir) + '/data/' + data_file_name + '.data')

    with open(data_file_path, 'r') as data_file:
        file_data = data_file.read()
        file_data = file_data.split(',')
        extension = file_data[0]

    file_stats = os.stat(filepath)

    last_accessed_time = datetime.fromtimestamp(file_stats.st_atime)
    last_modified_time = datetime.fromtimestamp(file_stats.st_mtime)
    last_status_change_time = datetime.fromtimestamp(file_stats.st_ctime)

    print(str(filename) + str(extension) + " info:" + "\n")
    print(f"Size: {file_stats.st_size} bytes")
    print(f"Mode: {file_stats.st_mode}")
    print(f"UID: {file_stats.st_uid}")
    print(f"GID: {file_stats.st_gid}")
    print(f"Device: {file_stats.st_dev}")
    print(f"INode: {file_stats.st_ino}")
    print(f"Number of hard links: {file_stats.st_nlink}")
    print(f"Last accessed: {last_accessed_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Last modified: {last_modified_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Last status change: {last_status_change_time.strftime('%Y-%m-%d %H:%M:%S')}")
    return


