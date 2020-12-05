from arguments import Arguments
from Headers.dos import Dos
from Headers.PE.portable_executable import PortableExecutable
from cli import ConsoleLineInterface
from CUI.cui import ConsoleUserInterface


class PyDump:
    def __init__(self, args):
        self._args = args

    def start(self):
        exe_file = ExeFile(self._args)
        exe_information = exe_file.get_information()
        if self._args.disassemble:
            ConsoleUserInterface(exe_information).cmdloop()
        else:
            output = ConsoleLineInterface(self._args)
            output.print(exe_information)


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

    def _parse(self):
        dos = Dos(self._exe_file)
        self._pe = PortableExecutable(self._exe_file, self._args.exe_file)
        self._close_file()

    def get_information(self):
        self._parse()
        return self._pe.get_fields()


def main():
    args = Arguments()
    PyDump(args).start()


if __name__ == '__main__':
    main()
