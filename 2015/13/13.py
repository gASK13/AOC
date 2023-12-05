import common
import itertools
class Seater:
    def __init__(self, lines):
        self.people = {}
        for line in lines:
            parts = line.split(' ')
            if parts[0] not in self.people:
                self.people[parts[0]] = {}
            self.people[parts[0]][parts[-1][:-1]] = int(parts[3]) * (-1 if parts[2] == 'lose' else 1)

    def add_person(self, name):
        self.people[name] = {}
        for person in self.people:
            self.people[person][name] = 0
            self.people[name][person] = 0

    def evaluate_arrangement(self, arrangement):
        happiness = 0
        for i in range(len(arrangement)):
            happiness += self.people[arrangement[i]][arrangement[i-1]]
            happiness += self.people[arrangement[i]][arrangement[(i+1)%len(arrangement)]]
        return happiness

    def find_best(self):
        return max([self.evaluate_arrangement(_) for _ in itertools.permutations(self.people.keys())])


assert Seater(common.Loader.load_lines('test')).find_best() == 330
seater = Seater(common.Loader.load_lines())
print(f'Part 1: {seater.find_best()}')
seater.add_person('Me')
print(f'Part 2: {seater.find_best()}')

