import os
import shutil

def write(file_path, string):
    if os.path.exists(file_path):
        os.remove(file_path)

    dir_path = os.path.dirname(file_path)
    if os.path.exists(dir_path) == False:
        os.makedirs(dir_path)

    fh = open(file_path, 'w')
    fh.write(string)
    fh.close()

def copy_file(src, dest):
    if os.path.exists(dest):
        os.remove(dest)

    dir_path = os.path.dirname(dest)
    if os.path.exists(dir_path) == False:
        os.makedirs(dir_path)

    shutil.copy(src, dest)

    