MACHINES_TYPES = {
    b'\x4c\x01': 'x86',
    b'\x00\x02': 'Intel Itanium',
    b'\x64\x86': 'x64'
}

SUBSYSTEM = {
    0: 'An unknown subsystem',
    1: 'Device drivers and native Windows processes',
    2: 'The Windows graphical user interface (GUI) subsystem',
    3: 'The Windows character subsystem',
    5: 'The OS/2 character subsystem',
    7: 'The Posix character subsystem',
    8: 'Native Win9x driver',
    9: 'Windows CE',
    10: 'An Extensible Firmware Interface (EFI) application',
    11: 'An EFI driver with boot services',
    12: 'An EFI driver with run-time services',
    13: 'An EFI ROM image',
    14: 'XBOX',
    16: 'Windows boot application.'
}
