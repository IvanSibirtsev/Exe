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

CHARACTERISTICS = [
    'IMAGE_FILE_RELOCS_STRIPPED',
    'IMAGE_FILE_EXECUTABLE_IMAGE',
    'IMAGE_FILE_LINE_NUMS_STRIPPED',
    'IMAGE_FILE_LOCAL_SYMS_STRIPPED',
    'IMAGE_FILE_AGGRESSIVE_WS_TRIM',
    'IMAGE_FILE_LARGE_ADDRESS_ AWARE',
    '',
    'IMAGE_FILE_BYTES_REVERSED_LO',
    'IMAGE_FILE_32BIT_MACHINE',
    'IMAGE_FILE_DEBUG_STRIPPED',
    'IMAGE_FILE_REMOVABLE_RUN_ FROM_SWAP',
    'IMAGE_FILE_NET_RUN_FROM_SWAP',
    'IMAGE_FILE_SYSTEM',
    'IMAGE_FILE_DLL',
    'IMAGE_FILE_UP_SYSTEM_ONLY',
    'IMAGE_FILE_BYTES_REVERSED_HI'
]

DLL_CHARACTERISTICS = [
    'Zero', 'Zero', 'Zero', 'Zero', ''
    'IMAGE_DLLCHARACTERISTICS_HIGH_ENTROPY_VA',
    'IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE',
    'IMAGE_DLLCHARACTERISTICS_FORCE_INTEGRITY',
    'IMAGE_DLLCHARACTERISTICS_NX_COMPAT',
    'IMAGE_DLLCHARACTERISTICS_NO_ISOLATION',
    'IMAGE_DLLCHARACTERISTICS_NO_SEH',
    'IMAGE_DLLCHARACTERISTICS_NO_BIND',
    'IMAGE_DLLCHARACTERISTICS_APPCONTAINER',
    'IMAGE_DLLCHARACTERISTICS_ WDM_DRIVER',
    'IMAGE_DLLCHARACTERISTICS_GUARD_CF',
    'IMAGE_DLLCHARACTERISTICS_TERMINAL_SERVER_AWARE'
]
