import math
import common

ores = {'ore': 0, 'clay': 1, 'obsidian': 2, 'geode': 3}

class Setup:
    def __init__(self, line, old=None):
        if old is None:
            self.id = int(line.split(':')[0].split(' ')[1])
            self.bots = [1, 0, 0, 0]
            self.ores = [0, 0, 0, 0]
            self.prices = [[0, 0, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0]]
            for bot in line.split(':')[1].strip().split('.'):
                words = bot.strip().split(' ')
                while len(words) > 3:
                    self.prices[ores[words[1]]][ores[words[-1]]] = int(words[-2])
                    words = words[:-3]
            self.minute = 0
            self.path = []
            self.maxes = [max([p[i] for p in self.prices]) for i in range(4)]
            self.maxes[3] = 9999 #we want a lot of geode ones
        else:
            self.id = old.id
            self.bots = [b for b in old.bots]
            self.ores = [o for o in old.ores]
            self.prices = old.prices
            self.minute = old.minute
            self.path = old.path + [old]
            self.maxes = old.maxes

    def pmax(self, maxmin):
        return self.ores[3] + self.bots[3] * (maxmin - self.minute) + sum([i for i in range(maxmin - self.minute)])

    def score(self, maxmin):
        return self.ores[3] + self.bots[3] * (maxmin - self.minute)

    def branch_all_states(self, maxmin):
        nstates = []
        for pi in range(4):
            price = self.prices[pi]
            # can we "wait" for all ingredients?
            canbuild = True
            steps = 0
            for i in range(4):
                if price[i] > 0 and self.bots[i] == 0:
                    canbuild = False
                elif self.bots[i] > self.maxes[i]:
                    canbuild = False
                elif price[i] > self.ores[i]:
                    steps = max(steps, math.ceil((price[i] - self.ores[i]) / self.bots[i]))
            # if so, wait, build and see
            if canbuild:
                nstate = Setup(None, self)
                for i in range(4):
                    nstate.ores[i] += nstate.bots[i] * (steps + 1)
                    nstate.ores[i] -= price[i]
                nstate.bots[pi] += 1
                nstate.minute += steps + 1
                if nstate.minute <= maxmin:
                    nstates.append(nstate)
        return reversed(nstates)

    def __str__(self):
        return f'BOT #{self.id} @ minute {self.minute} \nBots: {self.bots}\nOres: {self.ores}'

    def __repr__(self):
        return str(self)


def find_max(setup, minutes=24):
    buffer = [setup]
    max = setup
    i = 0
    while len(buffer) > 0:
        i+=1
        if i%10000 == 0:
            print(f'Buffer has {len(buffer)} items at roughly {buffer[0].minute} minutes. Max is {max.score(minutes)}')
        state = buffer.pop(0)
        if state.minute <= minutes:
            # find score
            if state.bots[3] > 0:
                if state.score(minutes) > max.score(minutes):
                    max = state
            buffer += [s for s in state.branch_all_states(minutes) if s.pmax(minutes) > max.score(minutes)]
    print(f'{max.id} > {max.score(minutes)}')
    return max.score(minutes)


assert find_max(Setup('Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.')) == 9
assert find_max(Setup('Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.')) == 12
print(f'FIRST PART IS {sum([s.id * find_max(s) for s in common.Loader.transform_lines(Setup)])}')

assert find_max(Setup('Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.'), 32) == 56
assert find_max(Setup('Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.'), 32) == 62
print(f'SECOND PART IS {[find_max(s, 32) for s in common.Loader.transform_lines(Setup)[:3]]}')




