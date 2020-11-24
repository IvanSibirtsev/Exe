import argparse
import sys
import os
# 'Git-2.26.2-64-bit.exe', 'AtomSetup-x64.exe', 'rufus-3.12.exe'


class Arguments:
    def __init__(self):
        self._parser = self._arg_parse()
        self.exe_file = Path(self._parser.exe_file).path

    @staticmethod
    def _arg_parse():
        d = {
            'git': 'Git-2.26.2-64-bit.exe',
            'rufus': 'rufus-3.12.exe',
            'atom': 'AtomSetup-x64.exe',
            'python': 'python-3.9.0-amd64.exe'
        }
        exe = d['python']
        parser = argparse.ArgumentParser(description='exe parser')
        parser.add_argument('-path', type=str, dest='exe_file',
                            default=exe, help='path to exe file.')
        return parser.parse_args()
# b'\x0b\x01'


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