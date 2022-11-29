import common
from collections import Counter


def move(_char, _shift):
    if _char == '-':
        return ' '
    newc = ord(_char) + _shift
    if newc > 122:
        newc -= 26
    return chr(newc)


class Room:
    def __init__(self, line):
        self._letters = '-'.join(line.split('[')[0].split('-')[:-1])
        self._number = int(line.split('[')[0].split('-')[-1])
        self._hash = line.split('[')[1].split(']')[0]

    def is_valid(self):
        return self._hash == self.compute_hash()

    def value(self):
        return self._number if self.is_valid() else 0

    def decrypt_name(self):
        if not self.is_valid():
            return '#####ERROR#####'
        shift = self._number % 26
        return ''.join([move(c, shift) for c in self._letters])

    def compute_hash(self):
        counter = Counter(self._letters.replace('-', ''))
        hash = ''
        while len(counter) > 0:
            add = []
            ltr = counter.most_common()[0]
            while len(counter) > 0 and counter.most_common()[0][1] == ltr[1]:
                add.append(counter.most_common()[0][0])
                counter.pop(counter.most_common()[0][0])
            add.sort()
            hash = hash + ''.join(add)

        return hash[:5]


assert Room('aaaaa-bbb-z-y-x-123[abxyz]').is_valid()
assert Room('a-b-c-d-e-f-g-h-987[abcde]').is_valid()
assert Room('not-a-real-room-404[oarel]').is_valid()
assert not Room('totally-real-room-200[decoy]').is_valid()

# Of the real rooms from the list above, the sum of their sector IDs is 1514.
rooms = common.Loader.transform_lines(Room)
print(f"Sum of valid rooms is {sum([r.value() for r in rooms])}")

assert Room('qzmt-zixmtkozy-ivhz-343[zimth]').decrypt_name() == 'very encrypted name'

for r in common.Loader.transform_lines(Room):
    if r.is_valid() and r.decrypt_name() == 'northpole object storage':
        print(f"{r.decrypt_name()} == {r.value()}")