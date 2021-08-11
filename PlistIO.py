import os
import shutil
import zipfile

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

    
## dir_path  : 准备要打包成zip的文件夹路径
## dest_path : 打包
def zip_dir(src_dir_path, dest_zip_path):
    if os.path.exists(dest_zip_path):
        os.remove(dest_zip_path)
    dest_dir_path = os.path.dirname(dest_zip_path)
    if os.path.exists(dest_dir_path) == False:
        os.makedirs(dest_dir_path)

    ## 标准化src_dir_path路径，带 path.sep 结尾
    src_dir_path = os.path.abspath(os.path.join(src_dir_path, ".")) + os.path.sep
    # print("src_dir_path=" + src_dir_path)
    # print("zip_dir -> dest_dir_path=" + dest_dir_path)
    # print("zip_dir -> dir_path=" + dir_path)
    pre_len = len(src_dir_path)
    dest_file = zipfile.ZipFile(dest_zip_path, "w")
    for parent, dirnames, filenames in os.walk(src_dir_path):
        for filename in filenames:
            item_path = os.path.join(parent, filename)
            item_name = item_path[pre_len:]
            dest_file.write(item_path, item_name)

    dest_file.close()