from CUI.action_types import ActionTypes


class Action:
    def __init__(self, dictionary):
        self._dictionary = dictionary

    def _action_definer(self):
        action_type = self._dictionary['action type']
        action_type_definer = {
            ActionTypes.WRITE: self._write_all,
            ActionTypes.WRITE_WITH_BOUNDS: self._write_with_bounds,
            ActionTypes.PRINT: self._print,
            ActionTypes.PRINT_WITH_BOUNDS: self._print_with_bounds
        }
        return action_type_definer[action_type]

    def _write_all(self, data):
        with open(self._dictionary['file'],
                  self._dictionary['write mode']) as file:
            for line in data:
                file.write(line + '\n')

    def _cut_data(self, data):
        left = self._dictionary['bounds'][0]
        right = self._dictionary['bounds'][1]
        return data[left:right]

    def _write_with_bounds(self, data):
        data = self._cut_data(data)
        self._write_all(data)

    def _print(self, data):
        for line in data:
            print(line)

    def _print_with_bounds(self, data):
        self._print(self._cut_data(data))

    def do(self, data):
        action = self._action_definer()
        action(data)
