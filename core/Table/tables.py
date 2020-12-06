from core.Table.export_table import ExportTable
from core.Table.import_table import ImportTable


class Tables:
    def __init__(self, rva, path, standard, data_directories):
        self._rva = rva
        self._path = path
        self._standard = standard
        self._data_directories = data_directories
        self._export_table = self._parse_export_table()
        self._import_table = self._parse_import_table()

    def _parse_export_table(self):
        address_and_size = self._data_directories.get_export_address_and_size()
        return ExportTable(self._rva, address_and_size, self._path)

    def get_export_table(self):
        return self._export_table

    def _parse_import_table(self):
        address_and_size = self._data_directories.get_import_address_and_size()
        magic = self._standard.get_magic()
        return ImportTable(self._rva, self._path, address_and_size, magic)

    def get_import_table(self):
        return self._import_table
