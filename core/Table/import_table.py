from core.Utils.byte_pareser import get_line, int_little


class ImportTable:
    _ZERO_STRUCT = b'\x00' * 20
    _ZERO_BYTES = b'\x00\x00'

    def __init__(self, rva, path, address_and_size, magic):
        self._rva = rva
        self._path = path
        self._address_and_size = address_and_size
        self._magic = magic
        self._import_table = self._parse()

    def _get_address_size(self):
        return map(lambda x: int_little(x), self._address_and_size)

    def get_fields(self):
        return self._import_table

    def _parse(self):
        address, size = self._get_address_size()
        if address == 0:
            return None
        result = []
        file = open(self._path, 'rb')
        file.seek(self._rva.rva_to_raw(address)[1])
        data = file.read(20)
        while data != self._ZERO_STRUCT:
            self._add(result, file, data)
            data = file.read(20)
        file.close()
        return result

    def _add(self, result, file, data):
        result.append({
            'Import Lookup Table RVA': int_little(data[:4]),
            'Time/date stamp': int_little(data[4:8]),
            'Forwarder chain': int_little(data[8:12]),
            'Name':
                get_line(file, self._rva.rva_to_raw(data[12:16])[1]),
            'Thunk table': int_little(data[16:20])
        })
        rva = self._rva.rva_to_raw(result[-1]['Thunk table'])[1]
        result[-1]['Functions'] = self._get_functions(file, rva)

    def _get_functions(self, file, address):
        result = {}
        start_address = file.tell()
        file.seek(address)
        size = 4 if self._magic == 'PE32' else 8
        lookup_table = int_little(file.read(size))
        while lookup_table != 0:
            if lookup_table < 8 * (16 ** (size * 2 - 1)):
                temp = file.tell()
                raw = self._rva.rva_to_raw(lookup_table)[1]
                file.seek(raw)
                name = get_line(file, raw + 2)
                hint = int_little(file.read(2))
                result[name] = hint
                file.seek(temp)
            lookup_table = int_little(file.read(size))
        file.seek(start_address)
        return result
