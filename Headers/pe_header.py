import struct
from datetime import datetime
import sys
from Headers.config import (MACHINES_TYPES, SUBSYSTEM,
                            CHARACTERISTICS, DLL_CHARACTERISTICS)


class PE:
    PE = b'PE\0\0'

    def __init__(self, file):
        self.file = file
        self._check_pe()
        self.image_file_header = self._file_header()
        self.optional_header = self._optional_header()

    def _file_header(self):
        return FileHeader(self.file.read(20)).get_fields()

    def _optional_header(self):
        optional_header_size = self.image_file_header['optional header size']
        return OptionalHeader(self.file.read(optional_header_size))

    def _check_pe(self):
        if self.file.read(4) != self.PE:
            print('Broken file. No "PE" in begin of PE header')
            sys.exit()


class FileHeader:
    def __init__(self, data):
        self._data = data

    def get_fields(self):
        (machine, number_of_sections, creating_time,
         pointer_to_symbol_table, number_of_symbols,
         optional_header_size,
         characteristic) = struct.unpack('HHIIIHH', self._data)
        machine = self._get_machine(self._data[:2])
        creating_time = datetime.fromtimestamp(creating_time)
        characteristic = self._characteristics(characteristic)
        fields = {
            'machine': machine,
            'number of sections': number_of_sections,
            'creating time': creating_time,
            'pointer to symbol table': pointer_to_symbol_table,
            'number of symbols': number_of_symbols,
            'optional header size': optional_header_size,
            'characteristic': characteristic
        }
        cli(fields)
        return fields

    @staticmethod
    def _get_machine(data):
        if data in MACHINES_TYPES:
            return MACHINES_TYPES[data]
        return 'Unknown'

    @staticmethod
    def _characteristics(data):
        return get_characteristic(data, CHARACTERISTICS)


class OptionalHeader:
    def __init__(self, data):
        self._data = data
        self._standard = self.standard()
        self.standard_fields = self._standard.get_fields()
        self._window_specific = self.window_specific()
        self.window_specific_fields = self._window_specific.get_fields()

    def standard(self):
        return OptionalHeaderStandard(self._data[:24])

    def window_specific(self):
        architecture = self._standard.get_architecture()
        return OptionalHeaderWindowSpecific(self._data, architecture)

    def data_directories(self):
        return OptionalDataDirectories(self._data)


class OptionalHeaderStandard:
    def __init__(self, data):
        self._data = data

    def get_fields(self):
        magic = self.get_architecture()
        base_of_data = 'Only PE32 field.'
        if magic == 'PE32':
            base_of_data = int_little(self._data[24:28])
        fields = {
            'magic': magic,
            'linker versions': (int_little(self._data[2:3]),
                                int_little(self._data[3:4])),
            'size of code': int_little(self._data[4:8]),
            'size of initialized data': int_little(self._data[8:12]),
            'size of uninitialized data': int_little(self._data[12:16]),
            'address of empty point': int_little(self._data[16:20]),
            'base of code': int_little(self._data[20:24]),
            'base of data': base_of_data
        }
        cli(fields)
        return fields

    def get_architecture(self):
        return 'PE64' if self._data[:2] == b'\x0b\x02' else 'PE32'


class OptionalHeaderWindowSpecific:
    def __init__(self, data, architecture):
        self._data = data
        self._architecture = architecture

    def get_fields(self):
        if self._architecture == 'PE32':
            offset = 4
            start = 28
        else:
            offset = 8
            start = 24
        data = self._data
        fields = {
            'image base:': int_little(data[start:start + offset]),
            'section alignment': int_little(data[32:36]),
            'file alignment': int_little(data[36:40]),
            'operating system versions': (int_little(data[40:42]),
                                          int_little(data[42:44])),
            'image versions': (int_little(data[44:46]),
                               int_little(data[46:48])),
            'subsystem versions': (int_little(data[48:50]),
                                   int_little(data[50:52])),
            'win 32 version value': int_little(data[52:56]),
            'size of image': int_little(data[56:60]),
            'size of headers': int_little(data[60:64]),
            'checksum': int_little(data[64:68]),
            'subsystem': self._get_subsystem(int_little(data[68:70])),
            'dll characteristic': self._parse_characteristics(data[70:72])
        }
        pos = 72 + offset
        fields['size of stack reserve'] = int_little(data[72: pos])
        fields['size of stack commit'] = int_little(data[pos: pos + offset])
        pos += offset
        fields['size of heap reserve'] = int_little(data[pos: pos + offset])
        pos += offset
        fields['size of heap commit'] = int_little(data[pos: pos + offset])
        pos += offset
        fields['loader flags'] = int_little(data[pos: pos + 4])
        pos += 4
        fields['number of rva and size'] = int_little(data[pos: pos + 4])
        cli(fields)
        return fields

    @staticmethod
    def _get_subsystem(data):
        return SUBSYSTEM[int(data)]

    @staticmethod
    def _parse_characteristics(data):
        data = int_little(data)
        return get_characteristic(int(data), DLL_CHARACTERISTICS)


class OptionalDataDirectories:
    def __init__(self, data):
        self._data = data


def cli(dictionary):
    for key in dictionary:
        string = str(dictionary[key])
        string = string.replace('[', '')
        string = string.replace(']', '')
        string = string.replace('(', '')
        string = string.replace(')', '')
        string = string.replace("'", '')
        print(key, string, sep=': ')


def int_little(data):
    return str(int.from_bytes(data, 'little'))


def get_characteristic(data, const):
    bin_str = bin(data).zfill(16)
    bin_str = [bin_str[-i - 1] == '1' for i in range(16)]
    ans = []
    for a, characteristic in zip(bin_str, const):
        if a:
            ans.append(characteristic)
    return ans
