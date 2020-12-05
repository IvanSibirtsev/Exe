from CUI.core.action_types import ActionTypes, ActionsWithFile


class Command:
    DEFAULT_BOUNDS = (0, 0)
    _DEFAULT_FILE = ''

    def __init__(self, user_input):
        self._user_input = user_input
        self._section = ''
        self._operator = ActionsWithFile.NOTHING
        self._file = self._DEFAULT_FILE
        self._bounds = self.DEFAULT_BOUNDS
        self._command_definer()

    def _command_definer(self):
        self._section = self._get_section_from_user_input()
        self._bounds = self._get_bounds_from_user_input()
        self._operator = self._get_operator_from_user_input()
        self._file = self._get_file_from_user_input()
        self._action_type = self._action_type_definer()

    def _action_type_definer(self):
        raw_action_type = (self._file == self._DEFAULT_FILE,
                           self._bounds == self.DEFAULT_BOUNDS)
        action = {
            (True, True): ActionTypes.PRINT,
            (True, False): ActionTypes.PRINT_WITH_BOUNDS,
            (False, True): ActionTypes.WRITE,
            (False, False): ActionTypes.WRITE_WITH_BOUNDS
        }
        return action[raw_action_type]

    def get_commands(self):
        return self._section, self._bounds, self._operator.value, self._file

    def get_dictionary(self):
        return {
            'section': self._section,
            'action type': self._action_type,
            'bounds': self._bounds,
            'file': self._file,
            'write mode': self._operator.value
        }

    def _get_section_from_user_input(self):
        return self._user_input.split()[0]

    def get_section(self):
        return self._section

    def _get_file_from_user_input(self):
        if not self._operator.value:
            return ''
        index = self._user_input.rfind('>')
        return self._user_input[index + 1:len(self._user_input)].lstrip()

    def _get_operator_from_user_input(self):
        if self._user_input.find('>>') != -1:
            return ActionsWithFile.ADD
        if self._user_input.find('>') != -1:
            return ActionsWithFile.WRITE
        return ActionsWithFile.NOTHING

    def _get_bounds_from_user_input(self):
        left = self._user_input.find('[')
        if left != -1:
            right = self._user_input.find(']')
            num_borders = self._user_input[left + 1:right]
            sep = num_borders.find('-')
            left_number = int(num_borders[0:sep])
            right_number = int(num_borders[sep + 1:len(num_borders)])
            return left_number, right_number
        return 0, 0
