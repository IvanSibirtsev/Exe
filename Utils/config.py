MACHINES_TYPES = {
    '0x1d3': 'AM33', '0x8664': 'x64',
    '0x1c0': 'ARM', '0xaa64': 'ARM64', '0x1c4': 'ARMNT',
    '0xebc': 'EBC',
    '0x14c': 'x86', '0x200': 'Intel Itanium',
    '0x9041': 'M32R',
    '0x266': 'MIPS16', '0x366': 'MIPSFPU', '0x466': 'MIPSFPU16',
    '0x1f0': 'POWERPC', '0x1f1': 'POWERPCFP',
    '0x166': 'R4000',
    '0x5032': 'RISCV32', '0x5064': 'RISCV64', '0x5128': 'RISCV128',
    '0x1a2': 'SH3', '0x1a3': 'SH3DSP', '0x1a6': 'SH4', '0x1a8': 'SH5',
    '0x1c2': 'THUMB',
    '0x169': 'WCEMIPSV2'
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

CHARACTERISTICS = [
    'RELOCS_STRIPPED',
    'EXECUTABLE_IMAGE',
    'LINE_NUMS_STRIPPED',
    'LOCAL_SYMS_STRIPPED',
    'AGGRESSIVE_WS_TRIM',
    'LARGE_ADDRESS_AWARE',
    '',
    'BYTES_REVERSED_LO',
    '32BIT_MACHINE',
    'DEBUG_STRIPPED',
    'REMOVABLE_RUN_FROM_SWAP',
    'NET_RUN_FROM_SWAP',
    'SYSTEM',
    'DLL',
    'UP_SYSTEM_ONLY',
    'BYTES_REVERSED_HI'
]

DLL_CHARACTERISTICS = [
    'Zero', 'Zero', 'Zero', 'Zero', ''
    'HIGH_ENTROPY_VA',
    'DYNAMIC_BASE',
    'FORCE_INTEGRITY',
    'NX_COMPAT',
    'NO_ISOLATION',
    'NO_SEH',
    'NO_BIND',
    'APPCONTAINER',
    'WDM_DRIVER',
    'GUARD_CF',
    'TERMINAL_SERVER_AWARE'
]
