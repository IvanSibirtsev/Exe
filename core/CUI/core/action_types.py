import enum


class ActionTypes(enum.Enum):
    WRITE = 'write'
    WRITE_WITH_BOUNDS = 'write with bounds'
    PRINT = 'print'
    PRINT_WITH_BOUNDS = 'print with bounds'


class ActionsWithFile(enum.Enum):
    ADD = 'a'
    WRITE = 'w'
    NOTHING = ''
