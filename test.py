import os
import io
import sys
import unittest
import datetime
from core.CUI.core.command import Command
from core.CUI.core.action_types import ActionTypes
from core.CUI.core.action import Action
from core.Headers.PE.portable_executable import PortableExecutable
from core.Headers.dos import Dos
import pydump
from core.Utils.arguments import Path
from ForTests.test_classes import Arguments


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


class TestAction(unittest.TestCase):
    def test_action_type_definer(self):
        dictionary = {
            'action type': ActionTypes.WRITE_WITH_BOUNDS,
            'file': 'for_test.txt',
            'write mode': 'w',
            'bounds': (0, 4)
        }
        data = 'data' * 3
        Action(dictionary).do(data)
        self.assertEqual(True, os.path.exists('for_test.txt'))
        with open('for_test.txt', 'r') as file:
            wrote_data = file.read()
        self.assertEqual(wrote_data, 'd\na\nt\na\n')
        os.remove('for_test.txt')


class TestExe(unittest.TestCase):
    def setUp(self):
        self.tested_file = 'ForTests/PEview.exe'
        git = open(self.tested_file, 'rb')
        dos = Dos(git)
        self.exe_file = PortableExecutable(git, self.tested_file).get_fields()
        git.close()

    def test_headers(self):
        headers = {
            'path': self.tested_file,
            'file header': '',
            'optional header': '',
            'section table': '',
            'export table': '',
            'import table': ''
        }
        self.assertEqual(self.exe_file.keys(), headers.keys())

    def test_file_header(self):
        file_header = self.exe_file['file header']
        fields = {
            'characteristic': [
                'RELOCS_STRIPPED', 'EXECUTABLE_IMAGE',
                'LINE_NUMS_STRIPPED', 'LOCAL_SYMS_STRIPPED',
                '32BIT_MACHINE'],
            'creating time': datetime.datetime(2011, 5, 17, 5, 18, 47),
            'machine': 'x86',
            'number of sections': 5,
            'number of symbols': 0,
            'optional header size': 224,
            'pointer to symbol table': 0}
        self.assertEqual(file_header, fields)

    def test_optional_header(self):
        optional_header = self.exe_file['optional header']
        zeroes = (b'\x00\x00\x00\x00', b'\x00\x00\x00\x00')
        fields = {
            'data directories': [
                zeroes, (b'dB\x01\x00', b'\xa0\x00\x00\x00'),
                (b'\x00\x00\x01\x00', b'\x00;\x00\x00'),
                zeroes, zeroes, zeroes, zeroes, zeroes, zeroes, zeroes, zeroes,
                zeroes,
                (b'\x04C\x01\x00', b'\xb4\x01\x00\x00'), zeroes, zeroes,
                zeroes],
            'standard': {
                'address of empty point': 4096,
                'base of code': 4096,
                'base of data': 0,
                'linker versions': (0, 38),
                'magic': 'PE32',
                'size of code': 33280,
                'size of initialized data': 33280,
                'size of uninitialized data': 0},
            'windows specific': {
                'checksum': 104208,
                'dll characteristic': [],
                'file alignment': 512,
                'image base': 4194304,
                'image versions': (0, 0),
                'loader flags': 0,
                'number of rva and size': 16,
                'operating system versions': (4, 0),
                'section alignment': 4096,
                'size of headers': 1024,
                'size of heap commit': 4096,
                'size of heap reserve': 1048576,
                'size of image': 86016,
                'size of stack commit': 65536,
                'size of stack reserve': 1048576,
                'subsystem': 'The Windows graphical user interface (GUI) '
                             'subsystem',
                'subsystem versions': (4, 0),
                'win 32 version value': 0}}
        self.assertEqual(optional_header, fields)

    def test_section_table(self):
        section_table = self.exe_file['section table']
        fields = {
            'characteristics': ['CNT_CODE', 'MEM_EXECUTE', 'MEM_READ'],
            'number of number lines': 0,
            'number of relocations': 0,
            'pointer to line numbers': 0,
            'pointer to raw data': 64000,
            'pointer to relocations': 0,
            'size of raw data': 3584,
            'virtual address': 81920,
            'virtual size': 3414}
        self.assertEqual(section_table['.idata'], fields)

    def test_export_table(self):
        export_table = self.exe_file['export table']
        fields = None
        self.assertEqual(export_table, fields)

    def test_import_table(self):
        import_table = self.exe_file['import table']
        fields = {
            'Forwarder chain': 0,
            'Functions': {
                'RegCloseKey': 560,
                'RegCreateKeyExA': 568,
                'RegDeleteKeyA': 573,
                'RegOpenKeyExA': 608,
                'RegQueryInfoKeyA': 615,
                'RegQueryValueExA': 621,
                'RegSetValueExA': 637},
            'Import Lookup Table RVA': 83128,
            'Name': 'ADVAPI32.dll',
            'Thunk table': 82692,
            'Time/date stamp': 0}
        self.assertEqual(import_table[0], fields)

    def test_export_table_for_dll(self):
        dll = 'ForTests/unistim.dll'
        dll_file = pydump.ExeFile(dll).get_information()
        export_table = dll_file['export table']
        fields = {
            'addresses of functions':
                ['0x1000', '0x9330', '0x933C', '0x9338'],
            'addresses of name ordinals': 82744,
            'addresses of names': 82728,
            'base': 1,
            'characteristics': '0x00',
            'name': 'unistim.dll',
            'name ordinals': [1, 2, 3, 4],
            'names': ['plugin_register',
                      'plugin_version',
                      'plugin_want_major',
                      'plugin_want_minor'],
            'number of functions': 4,
            'number of names': 4,
            'time date stamp': '0xFFFFFFFF',
            'version': '0.0'}
        self.assertEqual(export_table, fields)


class TestArguments(unittest.TestCase):
    def test_path(self):
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        incorrect_path = 'README.md'
        with self.assertRaises(SystemExit):
            Path(incorrect_path)
        incorrect_path = 'rngonvurtbv.zip'
        with self.assertRaises(SystemExit):
            Path(incorrect_path)
        sys.stdout = old_stdout
        output = buffer.getvalue()
        self.assertEqual('Work only with exe or dll. No .md\n'
                         f'No such file {incorrect_path}\n', output)


class TestPyDump(unittest.TestCase):
    def test_start_mode(self):
        args = Arguments()
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        pydump.PyDump(args).start()
        sys.stdout = old_stdout
        output = buffer.getvalue()
        self.assertEqual(True, output != '')


if __name__ == '__main__':
    unittest.main()
