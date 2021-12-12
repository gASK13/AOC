class Generator:
    def __init__(self, factor, start, mask):
        self.factor = factor
        self.last = start
        self.mask = mask

    def next(self):
        self.last = (self.last * self.factor) % 2147483647
        return self.last

    def trim_next(self):
        next = self.next()
        while next & self.mask > 0:
            next = self.next()
        return next & 65535


# TEST - 588
# a = Generator(16807, 65, 3)
# b = Generator(48271, 8921, 7)

a = Generator(16807, 703, 3)
b = Generator(48271, 516, 7)

matches = 0
for i in range(5000000):
    if a.trim_next() ^ b.trim_next() == 0:
        print(f'Found match at {i}th step.')
        matches += 1
print(matches)
