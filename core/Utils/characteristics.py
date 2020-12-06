from core.Utils.config import CHARACTERISTICS, DLL_CHARACTERISTICS, SECTION_FLAGS


class CharacteristicsDefiner:
    _hex = ['a', 'b', 'c', 'd', 'e', 'f']
    _NUMBER_SIMPLIFY = {
        '3': (1, 2), '5': (1, 4), '6': (2, 4),
        '7': (1, 2, 4), '9': (1, 8), 'a': (2, 8),
        'b': (1, 2, 8), 'c': (4, 8), 'd': (1, 4, 8),
        'e': (2, 4, 8), 'f': (1, 2, 4, 8)
    }
    _NAME_LEN = {
        'file': 4,
        'windows': 4,
        'section': 8
    }
    _CONFIG = {
        'file': CHARACTERISTICS,
        'windows': DLL_CHARACTERISTICS,
        'section': SECTION_FLAGS
    }

    def __init__(self, data, header_name):
        self._data = str(hex(data))
        self._header_name = header_name
        self._flags_len = self._len_definer()
        self._current_dictionary = self._characteristics_dictionary_definer()
        self._flags = self._normalization()
        self._characteristics = self._handle()

    def get_characteristics(self):
        return self._characteristics

    def _characteristics_dictionary_definer(self):
        return self._CONFIG[self._header_name]

    def _len_definer(self):
        hex_def = len('0x')
        return self._NAME_LEN[self._header_name] + hex_def

    def _normalization(self):
        flags = self._data
        if len(flags) < self._flags_len:
            flags = self._add_zeroes(flags)
        return flags

    def _add_zeroes(self, hex_string):
        zeroes_number = self._flags_len - len(hex_string)
        hex_string = hex_string.replace('0x', '0x' + '0' * zeroes_number)
        return hex_string

    def _handle(self):
        flags = self._flags[::-1]
        ans = []
        for flag, position in zip(flags, range(1, len(flags) - 1)):
            if flag == 'x':
                break
            if flag == '0':
                continue
            pair = (position, self._normalize_flag(flag))
            if pair in self._current_dictionary:
                ans.append(self._current_dictionary[pair])
            else:
                pairs = self._simplify(position, flag)
                for pair in pairs:
                    ans.append(self._current_dictionary[pair])
        return ans

    def _normalize_flag(self, flag):
        return flag if flag in self._hex else int(flag)

    def _simplify(self, position, flag):
        simplification = self._NUMBER_SIMPLIFY[str(flag)]

        pairs = [(position, number) for number in simplification]
        return pairs
