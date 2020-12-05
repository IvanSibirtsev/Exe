import argparse
import sys
import os


class Arguments:
    def __init__(self):
        self._parser = self._arg_parse()
        self.exe_file = Path(self._parser.exe_file).path
        self.disassemble = self._parser.disassemble
        self.file_header = self._parser.file_header
        self.optional_header = self._parser.optional_header
        self.section_header = self._parser.section_header
        self.export_table = self._parser.export_table
        self.import_table = self._parser.import_table
        self._if_all()

    @staticmethod
    def _arg_parse():
        exe = 'unistim.dll'
        exe = 'python-3.9.0-amd64.exe'
        d =  {
            'git': '.exe/Git-2.26.2-64-bit.exe',
            'rufus': '.exe/rufus-3.12.exe',
            'atom': '.exe/AtomSetup-x64.exe',
            'python': 'python-3.9.0-amd64.exe',
            's': '.exe/setup.exe'
        }
        exe = d['python']
        parser = argparse.ArgumentParser(description='exe parser')
        parser.add_argument('-path', type=str, dest='exe_file',
                            default=exe, help='path to exe file.')
        parser.add_argument('-d', '--disassemble', dest='disassemble',
                            action='store_true', default=False,
                            help='start to disassemble sections.')
        parser.add_argument('-f', '--file-header',action='store_true',
                            dest='file_header',
                            default=False, help='print file header')
        parser.add_argument('-o', '--optional-header', action='store_true',
                            dest='optional_header',
                            default=False, help='print optional header')
        parser.add_argument('-s', '--sections-header', action='store_true',
                            dest='section_header',
                            default=False, help='print section header')
        parser.add_argument('-e', '--export-table', action='store_true',
                            dest='export_table',
                            default=False, help='print export table')
        parser.add_argument('-i', '--import-table', action='store_true',
                            dest='import_table',
                            default=False, help='print import table')
        parser.add_argument('-x', action='store_true', default=True,
                            dest='all', help='print all information')
        return parser.parse_args()

    def _if_all(self):
        if self._parser.all:
            self.file_header = True
            self.optional_header = True
            self.section_header = True
            self.export_table = True
            self.import_table = True


class Path:
    def __init__(self, path):
        self.path = path
        self._check()

    def _check(self):
        if not os.path.exists(self.path):
            print(f'No such file {self.path}')
            sys.exit()
        extension = os.path.splitext(self.path)[1]
        if extension not in ['.exe', '.dll']:
            print(f'Work only with exe =. No {extension}')
            sys.exit()
