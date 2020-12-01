def int_little(data):
    return int.from_bytes(data, 'little')


def hex_from_bytes(byte_str, symbols_len=0):
    if not isinstance(byte_str, (str, bytes, bytearray)):
        raise TypeError

    if isinstance(byte_str, str):
        byte_str = bytes(byte_str)
    if not byte_str:
        return ''

    result = hex(int.from_bytes(byte_str, 'little'))[2:]\
        .upper().zfill(symbols_len)
    if len(result) % 2 == 1 and symbols_len == 0:
        result = '0' + result
    return '0x' + result


def get_line(f, address):
    temp_address = f.tell()
    f.seek(address, 0)
    letters = []
    let = f.read(1)
    while let != b'' and let != b'\x00':
        letters.append(let)
        let = f.read(1)
    f.seek(temp_address, 0)
    try:
        return b''.join(letters).decode('utf-8')
    except LookupError:
        return ''
