class DataDirectories:
    def __init__(self, data, magic, number_of_rva_and_sizes):
        self._data = data
        self._magic = magic
        self._number_of_rva_and_sizes = number_of_rva_and_sizes
        self._data_directories = self._parse()

    def get_export_address_and_size(self):
        return self._data_directories[0]

    def get_import_address_and_size(self):
        return self._data_directories[1]

    def _parse(self):
        start = 112
        if self._magic == 'PE32':
            start = 96
        data_directories = [(self._data[i * 8 + start: i * 8 + start + 4],
                            self._data[i * 8 + start + 4: i * 8 + start + 8]
                           ) for i in range(self._number_of_rva_and_sizes)]
        return data_directories

    def get_fields(self):
        return self._data_directories