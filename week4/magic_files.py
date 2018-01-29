import tempfile
import os
import itertools

def get_temp_file_path():
    fd, path = tempfile.mkstemp()
    os.close(fd)
    return path

class File:
    def __init__(self, path):
        self.path = path
        self.f = open(path, 'a+')
    
    def __str__(self):
        return self.path

    def __iter__(self):
        self.f.flush()
        self.f.seek(0)
        return self

    def __next__(self):
        line = self.f.readline()
        if not line:
            raise StopIteration("file is finished")
        return line

    def write(self, line):
        self.f.write(line)

    def __add__(self, other):
        if not isinstance(other, File):
            raise ValueError("Can't add File and {}".format(type(other)))
        
        both = File(get_temp_file_path())
        for line in itertools.chain(self, other):
            both.write(line)
        return both


if __name__ == '__main__':
    f1 = File("/tmp/f1.txt")
    f1.write('f1-line1\n')
    f1.write('f1-line2\n')

    f2 = File("/tmp/f2.txt")
    f1.write('f2-line1\n')
    f1.write('f2-line2\n')

    f3 = f1 + f2
    for line in f3:
        print(line, end='')