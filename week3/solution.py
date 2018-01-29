import sys

class FileReader:
    def __init__(self, fpath):
        try:
            self.f = open(fpath)
        except IOError:
            self.f = None

    def read(self):
        return self.f.read() if self.f else ''


if __name__ == '__main__':
    print(FileReader(sys.argv[1]).read(), end='')
