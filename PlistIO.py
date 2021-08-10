def write(file_path, string):
    fh = open(file_path, 'w')
    fh.write(string)
    fh.close()