number = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0E\xFC\xFE\xEE\xFE\xFE\xFE\xFE\xFE\xFE\x1A\x86\x82\xAA\x82\x82\x82\x82\x82\x82\x12\xFA\xFA\xBA\xBE\xBE\xFA\xBA\xBA\xBA\x1A\x82\x42\x82\x82\x82\x0A\x82\x82\xAA\x0A\xBE\xFA\xFA\xFA\xBA\x0A\xBA\xFA\xBA\x0A\x82\x82\x0A\x86\x82\x0A\x82\x82\x82\x0E\xFE\xFE\x0E\xFC\xFE\x0E\xFE\xFE\xFE')


def render(char):
    buffer = bytearray(8)
    step = char - 1
    if step == -1:
        step = 9
    for i in range(0, 8):
        buffer[i] = number[i*10 + step]

    return buffer