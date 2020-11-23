import struct
from datetime import datetime
import sys
from Headers.config import MACHINES_TYPES, SUBSYSTEM


class PE:
    PE = b'PE\0\0'

    def __init__(self, file):
        self.file = file
        self._check_pe()
        self.image_file_header = self._file_header()
        self.optional_header = self._optional_header()

    def _file_header(self):
        return FileHeader(self.file.read(20))

    def _optional_header(self):
        optional_header_size = self.image_file_header.optional_header_size
        return OptionalHeader(self.file.read(optional_header_size))

    def _check_pe(self):
        if self.file.read(4) != self.PE:
            print('Broken file. No "PE" in begin of PE header')
            sys.exit()


class FileHeader:
    def __init__(self, data):
        self._data = data
        self._image_file_header()

    def _image_file_header(self):
        (machine, self.number_of_sections, creating_time,
         self.pointer_to_symbol_table, self.number_of_sections,
         self.optional_header_size,
         characteristic) = struct.unpack('HHIIIIHH', self._data)
        self.machine = self._get_machine(machine)
        self.creating_time = datetime.fromtimestamp(creating_time).strftime
        self.characteristic = self._characteristics(characteristic)

    @staticmethod
    def _get_machine(data):
        if data in MACHINES_TYPES:
            return MACHINES_TYPES[data]
        return 'Unknown'

    @staticmethod
    def _characteristics(data):
        bin_str = bin(data).zfill(16)
        return [bin_str[-i - 1] == '1' for i in range(16)]


class OptionalHeader:
    def __init__(self, data):
        self._data = data
        self.standard = OptionalHeaderStandard(self._data[:24])

    def standard(self):
        return OptionalHeaderStandard(self._data[:24])

    def window_specific(self):
        architecture = self.standard.get_architecture()
        return OptionalHeaderWindowSpecific(self._data, architecture)

    def data_directories(self):
        return OptionalDataDirectories(self._data)


class OptionalHeaderStandard:
    def __init__(self, data):
        self._data = data

    def get_fields(self):
        magic = self.get_architecture()
        major_linker_version = int_little(self._data[2:3])
        minor_linker_version = int_little(self._data[3:4])
        size_of_code = int_little(self._data[4:8])
        size_of_initialized_data = int_little(self._data[8:12])
        size_of_uninitialized_data = int_little(self._data[12:16])
        address_of_empty_point = int_little(self._data[16:20])
        base_of_code = int_little(self._data[20:24])
        base_of_data = 'Only PE32 field.'
        if magic == 'PE32':
            base_of_data = int_little(self._data[24:28])
        return (major_linker_version, minor_linker_version,
                size_of_code, size_of_initialized_data,
                size_of_uninitialized_data, address_of_empty_point,
                base_of_code, base_of_data)

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

        image_base = int_little(data[start:start + offset])
        section_alignment = int_little(data[32:36])
        file_alignment = int_little(data[36:40])
        major_operating_system_version = int_little(data[40:42])
        minor_operating_system_version = int_little(data[42:44])
        major_image_version = int_little(data[44:46])
        minor_image_version = int_little(data[46:48])
        major_subsystem_version = int_little(data[48:50])
        minor_subsystem_version = int_little(data[50:52])
        win_32_version_value = int_little(data[52:56])
        size_of_image = int_little(data[56:60])
        size_of_headers = int_little(data[60:64])
        checksum = int_little(data[64:68])
        subsystem = self._get_subsystem(int_little(data[68:70]))
        dll_characteristic = self._parse_characteristics(data[70:72])
        position = 72 + offset
        size_of_stack_reserve = int_little(data[72: position])
        size_of_stack_commit = int_little(data[position: position + offset])
        position += offset
        size_of_heap_reserve = int_little(data[position: position + offset])
        position += offset
        size_of_heap_commit = int_little(data[position: position + offset])
        position += offset
        loader_flags = int_little(data[position: position + 4])
        position += 4
        number_of_rva_and_size = int_little(data[position: position + 4])
        return (image_base, section_alignment, file_alignment,
                major_operating_system_version, minor_operating_system_version,
                major_image_version, minor_image_version,
                major_subsystem_version, minor_subsystem_version,
                win_32_version_value, size_of_image, size_of_headers,
                checksum, subsystem, dll_characteristic,
                size_of_stack_reserve, size_of_stack_commit,
                size_of_heap_reserve, size_of_heap_commit, loader_flags,
                number_of_rva_and_size)

    @staticmethod
    def _get_subsystem(data):
        return SUBSYSTEM[data]

    @staticmethod
    def _parse_characteristics(data):
        binary_string = bin(int.from_bytes(data, 'little')).zfill(16)
        return [binary_string[-i - 1] == '1' for i in range(16)]


class OptionalDataDirectories:
    def __init__(self, data):
        self._data = data


def int_little(data):
    return str(int.from_bytes(data, 'little'))
