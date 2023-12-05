import common

test_data = {'Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.': {
    10: 140, 20: 140, 1: 14, 1000: 1120
},
    'Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.': {
        10: 160, 11: 176, 20: 176, 1: 16, 1000: 1056
    }}


class Reindeer:
    def __init__(self, line):
        self.name = line.split(' ')[0]
        self.speed = int(line.split(' ')[3])
        self.dash = int(line.split(' ')[6])
        self.rest = int(line.split(' ')[-2])
        self.distance = 0
        self.state = ['dash', self.dash]
        self.points = 0

    def run_for(self, ticks):
        for _ in range(ticks):
            self.tick()
        return self.distance

    def tick(self):
        if self.state[0] == 'dash':
            self.distance += self.speed
        self.state[1] -= 1
        if self.state[1] == 0:
            if self.state[0] == 'dash':
                self.state = ['rest', self.rest]
            else:
                self.state = ['dash', self.dash]


def race(reindeer, ticks):
    for _ in range(ticks):
        for r in reindeer:
            r.tick()
        max_distance = max([r.distance for r in reindeer])
        for r in reindeer:
            if r.distance == max_distance:
                r.points += 1
    return max([r.points for r in reindeer])


for t in test_data:
    for seconds in test_data[t]:
        assert Reindeer(t).run_for(seconds) == test_data[t][seconds]

assert race([Reindeer(_) for _ in test_data], 1000) == 689

print(f'Part 1: {max([Reindeer(_).run_for(2503) for _ in common.Loader.load_lines()])}')
print(f'Part 2: {race([Reindeer(_) for _ in common.Loader.load_lines()], 2503)}')
