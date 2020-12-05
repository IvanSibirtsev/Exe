import pydump
import unittest
from CUI.command import Command


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)


class TestCommand(unittest.TestCase):
    def test_simple(self):
        command = '.text [1024 - 4096] > text.txt'
        tested = Command(command).get_commands()
        self.assertEqual(tested, ('.text', (1024, 4096), 'w', 'text.txt'))

    def test_only_bounds(self):
        command = '.data [1024 - 4096]'
        tested = Command(command).get_commands()
        self.assertEqual(tested, ('.data', (1024, 4096), '', ''))

    def test_only_file(self):
        command = '.text > text.txt'
        tested = Command(command).get_commands()
        self.assertEqual(tested, ('.text', (0, 0), 'w', 'text.txt'))

    def test_add_to_file(self):
        command = '.text >> text.txt'
        tested = Command(command).get_commands()
        self.assertEqual(tested, ('.text', (0, 0), 'a', 'text.txt'))


if __name__ == '__main__':
    unittest.main()
