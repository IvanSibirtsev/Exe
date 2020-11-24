import sys


class Dos:
    MZ = b'MZ'

    def __init__(self, file):
        self.file = file
        self._check_mz()
        self.pe_header = self._pe_header()
        self.dos_stub_program = self._dos_stub_program()

    def _check_mz(self):
        if self.file.read(2) != self.MZ:
            print('Broken file. No "MZ" in begin of DOS header')
            sys.exit()

    def _pe_header(self):
        self.file.seek(60)
        pe_header = self.file.read(4)
        return int.from_bytes(pe_header, 'little')

    def _dos_stub_program(self):
        return self.file.read(self.pe_header - self.file.tell())

