import distorm3


class Disassembler:
    def __init__(self, exe_file):
        self._path = exe_file['path']
        self._section_table = exe_file['section table']
        self._options = distorm3.Decode32Bits
        self._offset = 0

    def disassembly(self, section_name):
        data = self._get_raw_data(section_name)
        opcodes = self._get_opcodes(data)
        return opcodes

    def _get_opcodes(self, data):
        opcode = []
        for (offset, size, instruction, hexdump) in distorm3.DecodeGenerator(
                self._offset, data, self._options):
            opcode.append(
                '%.8x: %-40s %s' % (offset, hexdump, instruction.lower()))
        return opcode

    def _get_raw_data(self, section_name):
        size = self._section_table[section_name]['size of raw data']
        position = self._section_table[section_name]['pointer to raw data']
        self._offset = position
        with open(self._path, 'rb') as file:
            file.seek(position)
            return file.read(size)
