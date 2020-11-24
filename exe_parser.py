from arguments import Arguments
from Headers.dos_header import Dos
from Headers.pe_header import PE


class ExeFile:
    def __init__(self, args):
        self._args = args
        self._exe_file = None
        self._open_file()
        self._dos = None

    def _open_file(self):
        self._exe_file = open(self._args.exe_file, 'rb')

    def _close_file(self):
        self._exe_file.close()

    def parse(self):
        dos = Dos(self._exe_file)
        print('PE Header:', dos.pe_header)
        print('DOS_Stub Program:', dos.dos_stub_program)
        pe = PE(self._exe_file)
        self._close_file()


def main():
    args = Arguments()
    exe_file = ExeFile(args)
    exe_file.parse()


if __name__ == '__main__':
    main()
