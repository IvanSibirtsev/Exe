from core.exe_file import ExeFile
from core.Utils.arguments import Arguments
from core.CUI.cli import ConsoleLineInterface
from core.CUI.cui import ConsoleUserInterface


class PyDump:
    def __init__(self, args):
        self._args = args

    def start(self):
        exe_file = ExeFile(self._args.exe_file)
        exe_information = exe_file.get_information()
        if self._args.disassemble:
            ConsoleUserInterface(exe_information).cmdloop()
        else:
            output = ConsoleLineInterface(self._args)
            output.print(exe_information)


def main():
    args = Arguments()
    PyDump(args).start()


if __name__ == '__main__':
    main()
