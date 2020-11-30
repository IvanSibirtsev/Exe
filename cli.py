class ConsoleLineInterface:
    _SPECIAL_FIELDS = ['Functions']

    def __init__(self, args, data):
        self._args = args
        self._data = data
        self.print_file_header()
        self.print_optional_header()
        self.print_sections()
        self.print_export_table()
        self.print_import_table()

    def print_file_header(self):
        file_header = self._data['file header']
        self.print_header_and_fields('File header', file_header, 0 )

    def print_optional_header(self):
        print('Optional header:')
        optional_header = self._data['optional header']
        for header in optional_header:
            if header == 'data directories':
                continue
            self.print_header_and_fields(header, optional_header[header], 1)

    def print_sections(self):
        print('Sections headers:')
        section_header = self._data['section table']
        for section in section_header:
            self.print_header_and_fields(section, section_header[section], 1)

    def print_export_table(self):
        export_table = self._data['export table']
        if not export_table:
            return
        self.print_header_and_fields('Export table', export_table, 0)

    def print_import_table(self):
        print('Import table:')
        import_table = self._data['import table']
        for lib in import_table:
            name = lib['Name']
            self.print_header_and_fields(name, lib, 1)

    def print_header_and_fields(self, name, data, deep):
        print('\t' * deep, name, ':', sep='')
        for field in data:
            if field in self._SPECIAL_FIELDS:
                self.print_header_and_fields(field, data[field], deep + 1)
                continue
            value = normalize(data[field])
            print('\t' * (deep + 1), field, ': ', value, sep='')



def normalize(value):
    string = str(value)
    for rep in ['[', ']', '(', ')', "'"]:
        string = string.replace(rep, '')
    return string
