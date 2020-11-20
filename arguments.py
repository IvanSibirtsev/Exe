import argparse
import sys
import os


class Arguments:
    def __init__(self):
        self._parser = self._arg_parse()
        self.exe_file = Path(self._parser.exe_file).path

    @staticmethod
    def _arg_parse():
        rufus = 'rufus-3.12.exe'
        parser = argparse.ArgumentParser(description='exe parser')
        parser.add_argument('-path', type=str, dest='exe_file',
                            default=rufus, help='path to exe file.')
        return parser.parse_args()


class Path:
    def __init__(self, path):
        self.path = path
        self._check()

    def _check(self):
        if not os.path.exists(self.path):
            print(f'No such file {self.path}')
            sys.exit()
        extension = os.path.splitext(self.path)[1]
        if extension != '.exe':
            print(f'Work only with exe =. No {extension}')
            sys.exit()