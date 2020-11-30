import struct
from datetime import datetime
from Utils.config import MACHINES_TYPES, CHARACTERISTICS
from Utils.byte_pareser import cli, int_little, get_characteristic

class FileHeader:
    def __init__(self, data):
        self._data = data
        self._number_of_sections = ''
        self._optional_header_size = ''
        self._file_header = self._parse()

    def get_number_of_sections(self):
        return self._number_of_sections

    def get_optional_header_size(self):
        return int(self._optional_header_size)

    def _parse(self):
        (machine, self._number_of_sections, creating_time,
         pointer_to_symbol_table, number_of_symbols,
         self._optional_header_size,
         characteristic) = struct.unpack('HHIIIHH', self._data)
        machine = self._get_machine(self._data[:2])
        creating_time = datetime.fromtimestamp(creating_time)
        characteristic = self._characteristics(characteristic)
        fields = {
            'machine': machine,
            'number of sections': self._number_of_sections,
            'creating time': creating_time,
            'pointer to symbol table': pointer_to_symbol_table,
            'number of symbols': number_of_symbols,
            'optional header size': self._optional_header_size,
            'characteristic': characteristic
        }
        return fields

    def get_fields(self):
        return self._file_header

    @staticmethod
    def _get_machine(data):
        data = hex((int_little(data)))
        if data in MACHINES_TYPES:
            return MACHINES_TYPES[data]
        return 'Unknown'

    @staticmethod
    def _characteristics(data):
        return get_characteristic(data, CHARACTERISTICS)
