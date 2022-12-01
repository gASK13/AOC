import common


def decompress(line, advanced=False):
    output = ''
    while len(line) > 0:
        splits = line.split('(', maxsplit=1)
        output += splits.pop(0)
        if len(splits) > 0:
            line = splits.pop(0)
            (markers, line) = line.split(')', maxsplit=1)
            pattern = line[:int(markers.split('x')[0])]
            if advanced:
                pattern = decompress(pattern, True)
            line = line[int(markers.split('x')[0]):]
            for i in range(int(markers.split('x')[1])):
                output += pattern
        else:
            line = ''
    return output


assert decompress('ADVENT') == 'ADVENT'
assert decompress('A(1x5)BC') == 'ABBBBBC'
assert decompress('(3x3)XYZ') == 'XYZXYZXYZ'
assert decompress('A(2x2)BCD(2x2)EFG') == 'ABCBCDEFEFG'
assert decompress('(6x1)(1x3)A') == '(1x3)A'
assert decompress('X(8x2)(3x3)ABCY') == 'X(3x3)ABC(3x3)ABCY'

print(f'Simple length is {len(decompress(common.Loader.load_lines()[0]))}')

assert decompress('(3x3)XYZ', True) == 'XYZXYZXYZ'
assert decompress('X(8x2)(3x3)ABCY', True) == 'XABCABCABCABCABCABCY'
assert decompress('(27x12)(20x12)(13x14)(7x10)(1x12)A', True) == ''.join(['A' for i in range(241920)])
assert len(decompress('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN', True)) == 445

print(f'Real length is {len(decompress(common.Loader.load_lines()[0], True))}')