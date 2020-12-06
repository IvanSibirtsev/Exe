from cmd import Cmd
import sys


class Console(Cmd):
    def __init__(self):
        Cmd.__init__(self)

    def cmdloop(self, intro=None):
        try:
            Cmd.cmdloop(self, intro)
        except KeyboardInterrupt:
            print('Exit.')
            sys.exit()
