from core.Utils.byte_pareser import int_little, hex_from_bytes, get_line


class ExportTable:
    def __init__(self, rva, address_and_size, path):
        self._rva = rva
        self._path = path
        self._address_and_size = address_and_size
        self._export_table = self._parse()

    def _parse(self):
        address, size = map(lambda x: int_little(x), self._address_and_size)
        if address == 0:
            return None
        address = self._rva.rva_to_raw(address)[1]
        file = open(self._path, 'rb')
        file.seek(address)
        data = file.read(40)
        export_table = {
            'characteristics': hex_from_bytes(data[:4]),
            'time date stamp': hex_from_bytes(data[4:8]),
            'version': (str(int_little(data[8:10])) + '.' +
                        str(int_little(data[10:12]))),
            'name': self._rva.rva_to_raw(data[12:16])[1],
            'base': int_little(data[16:20]),
            'number of functions': int_little(data[20:24]),
            'number of names': int_little(data[24:28]),
            'addresses of functions': self._rva.rva_to_raw(data[28:32])[1],
            'addresses of names': self._rva.rva_to_raw(data[32:36])[1],
            'addresses of name ordinals': self._rva.rva_to_raw(data[36:40])[1]
        }
        export_table['name'] = get_line(file, export_table['name'])
        self._parse_functions(file, export_table)
        self._parse_ordinals(file, export_table)
        self._parse_function_names(file, export_table)
        file.close()
        return export_table

    def _parse_functions(self, file, export_table):
        file.seek(export_table['addresses of names'], 0)
        array_data = file.read(export_table['number of names'] * 4)
        export_table['names'] = parse_data_to_array(
            array_data, 4,
            lambda x: get_line(file, self._rva.rva_to_raw(x)[1]))

    def _parse_ordinals(self, file, export_table):
        file.seek(export_table['addresses of name ordinals'])
        array_data = file.read(export_table['number of names'] * 2)
        export_table['name ordinals'] = parse_data_to_array(
            array_data, 2,
            lambda x: int_little(x) + 1)

    def _parse_function_names(self, file, export_table):
        file.seek(export_table['addresses of functions'])
        array_data = file.read(export_table['number of functions'] * 4)
        export_table['addresses of functions'] = parse_data_to_array(
            array_data, 4,
            lambda x: hex_from_bytes(x))

    def get_export_table(self):
        return self._export_table


def parse_data_to_array(data, cell_size: int, func):
    result = []
    if len(data) % cell_size != 0:
        raise ValueError("Length of data must be a multiple of cell_size")
    for i in range(len(data) // cell_size):
        result.append(func(data[i * cell_size:(i + 1) * cell_size]))
    return result
