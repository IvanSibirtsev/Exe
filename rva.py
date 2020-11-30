class RVA:
    def __init__(self, file_header, sections_table):
        self.file_header = file_header
        self.section_table = sections_table.get_fields()

    def rva_to_raw(self, rva):
        if isinstance(rva, bytes):
            rva = int.from_bytes(rva, 'little')
        if not isinstance(rva, int):
            raise TypeError('rva may be only int or bytes object')

        index_section = self._find_section(rva)
        if index_section != -1:
            pointer = 'pointer to raw data'
            current_point = self.section_table[index_section][pointer]
            current_va = self.section_table[index_section]['virtual address']
            return index_section, current_point + rva - current_va
        return index_section, rva

    def _find_section(self, rva):
        for i in self.section_table:
            start = self.section_table[i]['virtual address']
            end = start + self.section_table[i]['virtual size']
            if start <= rva < end:
                return i
        return -1
