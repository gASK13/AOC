import common

INPUT = {'children': 3,
         'cats': 7,
         'samoyeds': 2,
         'pomeranians': 3,
         'akitas': 0,
         'vizslas': 0,
         'goldfish': 5,
         'trees': 3,
         'cars': 2,
         'perfumes': 1}


class Sue:
    def __init__(self, line):
        self.num = int(line.split(': ')[0].split(' ')[1])
        self.items = {}
        for item, count in [_.split(': ') for _ in (': '.join(line.split(': ')[1:])).split(', ')]:
            self.items[item] = int(count)

    def is_valid(self):
        for item, count in self.items.items():
            if INPUT[item] != count:
                return False
        return True

    def is_valid_part2(self):
        for item, count in self.items.items():
            if item in ['cats', 'trees']:
                if INPUT[item] >= count:
                    return False
            elif item in ['pomeranians', 'goldfish']:
                if INPUT[item] <= count:
                    return False
            elif INPUT[item] != count:
                return False
        return True

    def __str__(self):
        return f'{self.num}: {self.items}'

    def __repr__(self):
        return self.__str__()

print('Part1: ' + str([s for s in common.Loader.transform_lines(Sue) if s.is_valid()]))
print('Part2: ' + str([s for s in common.Loader.transform_lines(Sue) if s.is_valid_part2()]))