from core.Headers.PE.portable_executable import PortableExecutable
from core.Headers.dos import Dos


class ExeFile:
    def __init__(self, path):
        self._path = path
        self._exe_file = None
        self._open_file()
        self._dos = None

    def _open_file(self):
        self._exe_file = open(self._path, 'rb')

    def _close_file(self):
        self._exe_file.close()

    def _parse(self):
        dos = Dos(self._exe_file)
        self._pe = PortableExecutable(self._exe_file, self._path)
        self._close_file()

    def get_information(self):
        self._parse()
        return self._pe.get_fields()
