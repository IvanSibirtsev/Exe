import sys
from core.Utils.byte_pareser import int_little


class Dos:
    MZ = b'MZ'

    def __init__(self, file):
        self._file = file
        self._check_mz()
        self._pe_header = self._pe_header()
        self._dos_stub_program = self._dos_stub_program()

    def _check_mz(self):
        if self._file.read(2) != self.MZ:
            print('Broken file. No "MZ" in begin of DOS header')
            sys.exit()

    def _pe_header(self):
        self._file.seek(60)
        pe_header = self._file.read(4)
        return int_little(pe_header)

    def get_pe_header(self):
        return self._pe_header

    def _dos_stub_program(self):
        return self._file.read(self._pe_header - self._file.tell())

    def get_dos_stub_program(self):
        return self._dos_stub_program
