import common
from colorama import Fore, Back, Style

class Machine:
    def __init__(self, line):
        self.result = line.split(']')[0][1:] #Take just the part in brackets
        self.turned_on = [idx for idx in range(len(self.result)) if self.result[idx] == '#']
        self.options = [tuple([int(it) for it in option[1:-1].split(',')]) for option in line.split(']')[1].split('{')[0].strip().split(' ')]

    def find_least_button_presses(self):
        # Goal is not to TURN ON but to TURN OFF what we have
        # State = "on", "press_count", "options left"
        # We assume that pressing something 2 times is ... wasteful (why would we do that?)
        buffer = [(set(self.turned_on), 0, set(self.options))]

        # Simple hash based "avoidance" of converging paths - sped up from minutes to seconds
        seen = set()
        while len(buffer) > 0:
            turned_on, press_count, options = buffer.pop(0)
            hsh = f'{tuple(sorted(turned_on))}-{tuple(sorted(options))}'
            if hsh not in seen:
                seen.add(hsh)
            else:
                continue

            if len(turned_on) == 0:
                return press_count

            for option in options:
                # if no overlap > skip! (like skippy)
                if len(set(option).intersection(turned_on)) > 0:
                    new_turned_on = turned_on.copy()
                    for pos in option:
                        if pos in new_turned_on:
                            new_turned_on.remove(pos)
                        else:
                            new_turned_on.add(pos)
                    new_options = options.copy()
                    new_options.remove(option)
                    buffer.append((new_turned_on, press_count + 1, new_options))
        raise Exception('No options found!')



    def __repr__(self):
        return f'(result={self.result}, turned_on={self.turned_on}, options={self.options})'

    def __str__(self):
        return self.__repr__()

def fix_machine(line):
    m = Machine(line)
    return m.find_least_button_presses()

def part_one(lines):
    return sum([fix_machine(line) for line in lines])



test_data = {
    '[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}' : 2,
    '[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}' : 3,
    '[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}' : 2
}

for t in test_data:
    assert fix_machine(t) == test_data[t]

print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Style.RESET_ALL}')
