from common.loader import Loader


def get_common(_i, _bins, swap = False):
    counts = [bin[_i] for bin in _bins]
    if swap:
        return '0' if counts.count('1') >= counts.count('0') else '1'
    return '1' if counts.count('1') >= counts.count('0') else '0'


def filter_by_bit(_i, _bins, _bit):
    # keep one left
    if len(_bins) == 1:
        return _bins

    ret = []
    for bin in _bins:
        if bin[_i] == _bit:
            ret.append(bin)
    return ret


bins = Loader.load_lines()
digits = len(bins[0])

print(int(''.join([get_common(i, bins) for i in range(digits)]), 2) *
      int(''.join([get_common(i, bins, swap=True) for i in range(digits)]), 2))

ox = [b for b in bins]
co2 = [b for b in bins]
for i in range(digits):
    ox = filter_by_bit(i, ox, get_common(i, ox))
    co2 = filter_by_bit(i, co2, get_common(i, co2, swap=True))

print(ox)
print(co2)
print(int(ox[0], 2) * int(co2[0], 2))


