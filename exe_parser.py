from arguments import Arguments
from Headers.dos import Dos
from Headers.PE.portable_executable import PortableExecutable
from cli import ConsoleLineInterface


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
        pe = PortableExecutable(self._exe_file, self._args.exe_file)
        self._close_file()
        cli = ConsoleLineInterface(self._args, pe.get_fields())
        cli.print()


def main():
    args = Arguments()
    exe_file = ExeFile(args)
    exe_file.parse()


if __name__ == '__main__':
    main()
