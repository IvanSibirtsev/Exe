from Utils.byte_pareser import int_little
from Utils.config import SUBSYSTEM
from Utils.characteristics import CharacteristicsDefiner

class WindowsSpecific:
    def __init__(self, data, magic):
        self._data = data
        self._magic = magic
        self._number_of_rva_and_size = ''
        self._windows_specific = self._parse()

    def get_number_of_rva_and_size(self):
        return self._number_of_rva_and_size

    def _parse(self):
        if self._magic == 'PE32':
            offset = 4
            start = 28
        else:
            offset = 8
            start = 24
        data = self._data
        fields = {
            'image base': int_little(data[start:start + offset]),
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
        self._number_of_rva_and_size = fields['number of rva and size']
        return fields

    def get_fields(self):
        return self._windows_specific

    @staticmethod
    def _get_subsystem(data):
        return SUBSYSTEM[data]

    @staticmethod
    def _parse_characteristics(data):
        data = int_little(data)
        return CharacteristicsDefiner(data, 'windows').get_characteristics()