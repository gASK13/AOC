import common


# Example of a case:
# - I start with CRnCaSiRnBSi
# CRn can be reached from H or O and differs after so I need to find options that produce "afterwards"
# or from end???

class LittleChemist:
    def __init__(self, lines, electron = False):
        self.molecules = {lines[-1]} if not electron else {'e'}
        self.target = None if not electron else lines[-1]
        self.reactions = {}
        self.seen = {lines[-1]} if not electron else {'e'}
        for line in lines[:-2]:
            source, target = line.split(' => ')
            if source not in self.reactions:
                self.reactions[source] = []
            self.reactions[source].append(target)

    def combine(self):
        _products = set()
        for molecule in self.molecules:
            for source, targets in self.reactions.items():
                for i in range(len(molecule) - len(source) + 1):
                    if molecule[i:i+len(source)] == source:
                        for target in targets:
                            _products.add(molecule[:i] + target + molecule[i+len(source):])
        self.molecules = _products
        return len(self.molecules)

    def produce(self):
        steps = 0
        while self.target not in self.molecules:
            steps += 1
            print(f'Before {steps} steps, {len(self.molecules)} molecules, {len(self.seen)} seen')
            self.combine()
        return steps


assert LittleChemist(common.Loader.load_lines('test1')).combine() == 4
assert LittleChemist(common.Loader.load_lines('test2')).combine() == 7
print(f'Part 1: {LittleChemist(common.Loader.load_lines()).combine()}')

assert LittleChemist(common.Loader.load_lines('test3'), True).produce() == 3
assert LittleChemist(common.Loader.load_lines('test4'), True).produce() == 6

print(f'Part 2: {LittleChemist(common.Loader.load_lines(), True).produce()}')
