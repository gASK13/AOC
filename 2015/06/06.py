import common


class Lights:
    def __init__(self):
        self.lights = [[0 for i in range(1000)] for j in range(1000)]

    def run(self, command):
        if command.startswith('toggle'):
            value = None
        else:
            value = 1 if command.split(' ')[1] == 'on' else 0
        sx, sy = [int(x) for x in command.split(' ')[-3].split(',')]
        ex, ey = [int(x) for x in command.split(' ')[-1].split(',')]
        for y in range(sy, ey + 1):
            for x in range(sx, ex + 1):
                self.lights[y][x] = value if value is not None else 1 - self.lights[y][x]

    def run_new(self, command):
        if command.startswith('toggle'):
            value = +2
        else:
            value = +1 if command.split(' ')[1] == 'on' else -1
        sx, sy = [int(x) for x in command.split(' ')[-3].split(',')]
        ex, ey = [int(x) for x in command.split(' ')[-1].split(',')]
        for y in range(sy, ey + 1):
            for x in range(sx, ex + 1):
                self.lights[y][x] = max(self.lights[y][x] + value, 0)

    def count(self):
        return sum([sum(x) for x in self.lights])


def run_lights(commands, new=False):
    l = Lights()
    for command in commands:
        l.run_new(command) if new else l.run(command)
    return l.count()


test_data = [(['turn on 0,0 through 3,3', 'turn off 499,499 through 500,500'], 16, 16),
             (['turn on 0,0 through 3,3', 'toggle 0,0 through 1,1'], 12, 24),
             (['turn on 0,0 through 3,3', 'turn on 10,10 through 11,11'], 20, 20),
             (['turn on 0,0 through 999,999', 'toggle 0,0 through 999,0', 'turn off 499,499 through 500,500'], 998996, 1001996),
             (['turn on 0,0 through 3,3', 'toggle 0,0 through 999,0'], 1008, 2016)
             ]

for cmd, res, res_new in test_data:
    assert run_lights(cmd) == res
    assert run_lights(cmd, True) == res_new

print(f'Light count is {run_lights(common.Loader.load_lines())}')
print(f'Light count new is {run_lights(common.Loader.load_lines(), True)}')
