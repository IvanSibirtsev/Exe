from Headers.PE.Headers.OptionalHeaders.standard import Standard
from Headers.PE.Headers.OptionalHeaders.windows_specific import WindowsSpecific
from Headers.PE.Headers.OptionalHeaders.data_directories import DataDirectories


class OptionalHeader:
    def __init__(self, data):
        self._data = data
        self._optional_header = {}
        self._standard = self._make_standard()
        self._magic = self._standard.get_magic()
        self._windows_specific = self._make_windows_specific()
        self._data_directories = self._make_data_directories()
        self._make_fields_dictionary()

    def _make_standard(self):
        return Standard(self._data[:24])

    def get_standard(self):
        return self._standard

    def _make_windows_specific(self):
        return WindowsSpecific(self._data, self._magic)

    def get_windows_specific(self):
        return self._windows_specific

    def _make_data_directories(self):
        number = self._windows_specific.get_number_of_rva_and_size()
        return DataDirectories(self._data, self._magic, number)

    def get_data_directories(self):
        return self._data_directories

    def _make_fields_dictionary(self):
        standard_fields = self._standard.get_fields()
        windows_specific_fields = self._windows_specific.get_fields()
        data_directories_fields = self._data_directories.get_fields()
        self._optional_header['standard'] = standard_fields
        self._optional_header['windows specific'] = windows_specific_fields
        self._optional_header['data directories'] = data_directories_fields

    def get_fields(self):
        return self._optional_header