import common


class BurrowState:
    def __init__(self):
        self.room = {'A': [], 'B': [], 'C': [], 'D': []}
        self.corridor = [None for _ in range(11)]
        self.connections = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
        self.costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
        self.cost = 0
        self.room_size = 2

    @staticmethod
    def from_diagram(diagram, extended=False):
        burrow = BurrowState()
        burrow.room['A'].append(diagram[3][1])
        burrow.room['B'].append(diagram[3][3])
        burrow.room['C'].append(diagram[3][5])
        burrow.room['D'].append(diagram[3][7])
        if extended:
            burrow.room_size = 4
            burrow.room['A'].append('D')
            burrow.room['A'].append('D')
            burrow.room['B'].append('B')
            burrow.room['B'].append('C')
            burrow.room['C'].append('A')
            burrow.room['C'].append('B')
            burrow.room['D'].append('C')
            burrow.room['D'].append('A')
        burrow.room['A'].append(diagram[2][3])
        burrow.room['B'].append(diagram[2][5])
        burrow.room['C'].append(diagram[2][7])
        burrow.room['D'].append(diagram[2][9])
        return burrow

    def deep_copy(self):
        other = BurrowState()
        other.room = {k: [item for item in self.room[k]] for k in self.room}
        other.corridor = [i for i in self.corridor]
        other.cost = self.cost
        other.room_size = self.room_size
        return other

    def get_cost(self):
        return self.cost

    def is_solved(self):
        return all([c is None for c in self.corridor]) and all([all([v == k for v in self.room[k]]) for k in self.room])

    def make_moves(self):
        # try to move from rooms to coridoor
        options = []
        for k in self.room:
            if any(v != k for v in self.room[k]):
                # try to move out first
                options += self.__walk_corridor(k, -1)
                options += self.__walk_corridor(k, 1)
        for i in range(len(self.corridor)):
            k = self.corridor[i]
            if k is not None and all(v == k for v in self.room[k]):
                # try to move to the room (see if way is clear)
                if all([x is None for x in self.corridor[min(i + 1, self.connections[k]):max(i, self.connections[k] + 1)]]):
                    nb = self.deep_copy()
                    nb.corridor[i] = None
                    nb.cost += abs(i - self.connections[k]) * self.costs[k]
                    nb.cost += (self.room_size - len(nb.room[k])) * self.costs[k]
                    nb.room[k].append(k)
                    options.append(nb)

        return options

    def __walk_corridor(self, k, direction):
        nb = self.deep_copy()
        item = nb.room[k].pop()
        nb.cost += (self.room_size - len(nb.room[k])) * self.costs[item]
        options = []
        idx = self.connections[k]
        while len(self.corridor) > idx >= 0:
            if idx not in self.connections.values():
                if nb.corridor[idx] is None:
                    nb_l = nb.deep_copy()
                    nb_l.corridor[idx] = item
                    nb_l.cost += abs(self.connections[k] - idx) * self.costs[item]
                    options.append(nb_l)
                else:
                    break
            idx += direction
        return options

    def __key(self):
        hsh = ''.join([k if k is not None else 'X' for k in self.corridor]) + '#'
        hsh += ''.join(self.room['A']) + '#'
        hsh += ''.join(self.room['B']) + '#'
        hsh += ''.join(self.room['C']) + '#'
        hsh += ''.join(self.room['D'])
        return hsh

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if not isinstance(other, BurrowState):
            return NotImplemented
        return self.__key() == other.__key()


def solve(file=None, extended=False):
    burrows = [BurrowState.from_diagram(common.Loader.load_matrix(file), extended=extended)]
    seen = set()
    iter = 0
    while len(burrows) > 0:
        burrows.sort(key=BurrowState.get_cost, reverse=True)
        b = burrows.pop()
        if b not in seen:
            seen.add(b)
            if b.is_solved():
                return b.cost
            else:
                burrows += b.make_moves()
            iter += 1
            if iter % 1000 == 0:
                print(f'Lowest cost is {b.cost}, options is {len(burrows) + 1}')
    raise RuntimeError('COULD NOT SOLVE?')


# Part one was solved by hand, part two is "walk the graph" solution which is ... expensive :(
assert solve('test.txt') == 12521
assert solve() == 10607
assert solve('test.txt', extended=True) == 44169
print(f'REAL PT 2 {solve(extended=True)}')
