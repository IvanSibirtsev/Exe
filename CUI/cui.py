from cmd import Cmd
import sys
from disassembler import Disassembler
from CUI.command import Command
from CUI.action import Action


class Console(Cmd):
    def __init__(self):
        Cmd.__init__(self)

    def cmdloop(self, intro=None):
        try:
            Cmd.cmdloop(self, intro)
        except KeyboardInterrupt:
            print('Exit.')
            sys.exit()


class ConsoleUserInterface(Console):
    def __init__(self, exe_inf):
        Console.__init__(self)
        self.prompt = 'disassembler> '
        self._inf = exe_inf
        self._sections = self._sections()
        self.intro = ('Default Disassembler architecture is x86 (32 bits).\n' +
                      f'Current sections: {self._sections}')

    def _sections(self):
        return [s for s in self._inf['section table'].keys()]

    def default(self, user_input):
        if user_input == 'sections':
            sections = self._inf['section table'].keys()
            for section in sections:
                print(section, end=' ')
            print()
        command = Command(user_input)
        section = command.get_section()
        disassembler = Disassembler(self._inf)
        data = disassembler.disassembly(section)
        action = Action(command.get_dictionary())
        action.do(data)
