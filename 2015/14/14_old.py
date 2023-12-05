# Old version of Day 14, kept for posterity
import common

test_data = {'Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.': {
        10: 140, 20: 140, 1: 14, 1000: 1120
    },
    'Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.': {
        10:160, 11:176, 20: 176, 1: 16, 1000: 1056
    }}


class Reindeer:
    def __init__(self, line):
        self.name = line.split(' ')[0]
        self.speed = int(line.split(' ')[3])
        self.dash = int(line.split(' ')[6])
        self.rest = int(line.split(' ')[-2])

    def run_for(self, _secs):
        if _secs < 0:
            raise ValueError('Seconds must be positive')
        if _secs < self.dash:
            distance = self.speed * _secs
        else:
            distance = (self.speed * self.dash) * (_secs // (self.dash + self.rest))
            _s = _secs % (self.dash + self.rest)
            if 0 < _s:
                distance += self.speed * min(_s, self.dash)
        print(f'{self.name} ran {distance} km in {_secs} seconds')
        return distance


for t in test_data:
    reindeer = Reindeer(t)
    for seconds in test_data[t]:
        assert reindeer.run_for(seconds) == test_data[t][seconds]

print(f'Part 1: {max([Reindeer(_).run_for(2503) for _ in common.Loader.load_lines()])}')