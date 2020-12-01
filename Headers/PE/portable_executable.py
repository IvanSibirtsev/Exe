import sys
from rva import RVA
from Table.tables import Tables
from Headers.PE.Headers.file_header import FileHeader
from Headers.PE.Headers.optional_header import OptionalHeader
from Headers.PE.Headers.section_header import SectionTable


class PortableExecutable:
    PE_SIGNATURE = b'PE\0\0'

    def __init__(self, file, path):
        self.file = file
        self._path = path
        self.pe = {}
        self._check_signature()
        self._fields = {}
        self._file_header = self._make_file_header()
        self._optional_header = self._make_optional_header()
        self._section_table = self._make_section_table()
        self._tables = self._make_tables()
        self._export_table = self._get_export_table()
        self._import_table = self._get_import_table()

    def _check_signature(self):
        if self.file.read(4) != self.PE_SIGNATURE:
            print('Broken file. No "PE" in begin of PE header')
            sys.exit()

    def _make_file_header(self):
        return FileHeader(self.file.read(20))

    def _make_optional_header(self):
        optional_header_size = self._file_header.get_optional_header_size()
        return OptionalHeader(self.file.read(optional_header_size))

    def _make_section_table(self):
        section_size = 40
        number_of_sections = self._file_header.get_number_of_sections()
        return SectionTable(self.file.read(number_of_sections * section_size))

    def _get_rva(self):
        return RVA(self._file_header, self._section_table)

    def _make_tables(self):
        rva = self._get_rva()
        standard = self._optional_header.get_standard()
        data_directories = self._optional_header.get_data_directories()
        return Tables(rva, self._path, standard, data_directories)

    def _get_export_table(self):
        export_table = self._tables.get_export_table()
        return export_table

    def _get_import_table(self):
        import_table = self._tables.get_import_table()
        return import_table

    def _merge_all_fields(self):
        self._fields['file header'] = self._file_header.get_fields()
        self._fields['optional header'] = self._optional_header.get_fields()
        self._fields['section table'] = self._section_table.get_fields()
        self._fields['export table'] = self._export_table.get_export_table()
        self._fields['import table'] = self._import_table.get_fields()

    def get_fields(self):
        self._merge_all_fields()
        return self._fields
