from core.Utils.byte_pareser import int_little
from core.Utils.characteristics import CharacteristicsDefiner


class SectionTable:
    def __init__(self, data):
        self._data = data
        self._section_table = self._make_fields()

    def _make_fields(self):
        sections = {}
        data = self._data
        for i in range(len(data) // 40):
            pos = i * 40
            name = data[pos:pos + 8].strip(b'\x00').decode('utf-8')
            sections[name] = Section(data, pos).get_section()
        return sections

    def get_fields(self):
        return self._section_table


class Section:
    def __init__(self, data, pos):
        self._data = data
        self._pos = pos
        self._section = self._parse()

    def get_section(self):
        return self._section

    def _parse(self):
        data = self._data
        pos = self._pos
        fields = {
            'virtual size': int_little(data[pos + 8:pos + 12]),
            'virtual address': int_little(data[pos + 12:pos + 16]),
            'size of raw data': int_little(data[pos + 16:pos + 20]),
            'pointer to raw data': int_little(data[pos + 20:pos + 24]),
            'pointer to relocations': int_little(data[pos + 24:pos + 28]),
            'pointer to line numbers': int_little(data[pos + 28:pos + 32]),
            'number of relocations': int_little(data[pos + 32:pos + 34]),
            'number of number lines': int_little(data[pos + 34:pos + 36]),
            'characteristics': self._parse_characteristics(
                data[pos + 36:pos + 40])
        }

        return fields

    @staticmethod
    def _parse_characteristics(data):
        flags = int_little(data)
        return CharacteristicsDefiner(flags, 'section').get_characteristics()
