class ConsoleLineInterface:
    _SPECIAL_FIELDS = ['Functions']

    def __init__(self, args):
        self._args = args
        self._data = None

    def print(self, data):
        self._data = data
        if self._args.file_header:
            self._print_file_header()
        if self._args.optional_header:
            self._print_optional_header()
        if self._args.section_header:
            self._print_sections()
        if self._args.export_table:
            self._print_export_table()
        if self._args.import_table:
            self._print_import_table()

    def _print_file_header(self):
        file_header = self._data['file header']
        self._print_header_and_fields('File header', file_header, 0)

    def _print_optional_header(self):
        print('Optional header:')
        optional_header = self._data['optional header']
        for header in optional_header:
            if header == 'data directories':
                continue
            self._print_header_and_fields(header, optional_header[header], 1)

    def _print_sections(self):
        print('Sections headers:')
        section_header = self._data['section table']
        for section in section_header:
            self._print_header_and_fields(section, section_header[section], 1)

    def _print_export_table(self):
        export_table = self._data['export table']
        if not export_table:
            return
        self._print_header_and_fields('Export table', export_table, 0)

    def _print_import_table(self):
        import_table = self._data['import table']
        if not import_table:
            return
        print('Import table:')
        for lib in import_table:
            name = lib['Name']
            self._print_header_and_fields(name, lib, 1)

    def _print_header_and_fields(self, name, data, deep):
        print('\t' * deep, name.lower(), ':', sep='')
        for field in data:
            if field in self._SPECIAL_FIELDS:
                self._print_header_and_fields(field, data[field], deep + 1)
                continue
            value = normalize(data[field])
            print('\t' * (deep + 1), field, ': ', value, sep='')


def normalize(value):
    string = str(value)
    for rep in ['[', ']', '(', ')', "'"]:
        string = string.replace(rep, '')
    return string
