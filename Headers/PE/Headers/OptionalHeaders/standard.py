from Utils.byte_pareser import int_little

class Standard:
    def __init__(self, data):
        self._data = data
        self._magic = ''
        self._standard = self._parse()

    def get_magic(self):
        return self._magic

    def _parse(self):
        self._magic = self._define_magic()
        base_of_data = 'Only PE32 field.'
        if self._magic == 'PE32':
            base_of_data = int_little(self._data[24:28])
        fields = {
            'magic': self._magic,
            'linker versions': (int_little(self._data[2:3]),
                                int_little(self._data[3:4])),
            'size of code': int_little(self._data[4:8]),
            'size of initialized data': int_little(self._data[8:12]),
            'size of uninitialized data': int_little(self._data[12:16]),
            'address of empty point': int_little(self._data[16:20]),
            'base of code': int_little(self._data[20:24]),
            'base of data': base_of_data
        }
        return fields

    def get_fields(self):
        return self._standard

    def _define_magic(self):
        return 'PE64' if self._data[:2] == b'\x0b\x02' else 'PE32'