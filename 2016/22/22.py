import common


class NodeHolder:
    def __init__(self, lines=None, other=None, source=None, target=None):
        if lines is not None:
            self.nodes = {}
            for line in lines[2:]:
                n = self.parse_node(line)
                self.nodes[n[0]] = n
            self.data = (max([x for (x, y) in self.nodes.keys() if y == 0]), 0)
            self.steps = 0
            self.goal = (0, 0)
        elif other is not None and source is not None and target is not None:
            self.nodes = {}
            for n in other.nodes.values():
                self.nodes[n[0]] = (n[0], n[1], n[2])
            self.nodes[target] = (target, self.nodes[target][1], self.nodes[target][2] + self.nodes[source][2])
            self.nodes[source] = (source, self.nodes[source][1], 0)
            self.data = other.data if other.data != source else target
            self.steps = other.steps + 1
            self.goal = other.goal
        else:
            raise Exception("What are you doing?")

    def __str__(self):
        return f"@{self.steps} steps -> {self.data} ({self.get_zero()})"

    def get_zero(self):
        for n in self.nodes.values():
            if n[2] == 0:
                return n[0]
        return "NONE"

    def get_hash(self):
        return f'{self.data}#{self.get_zero()}'

    def parse_node(self, line):
        items = line.split()
        pos = tuple([int(i[1:]) for i in items[0].split('-')[1:]])
        size = int(items[1][:-1])
        used = int(items[2][:-1])
        return (pos, size, used)

    def get_states(self):
        return [NodeHolder(other=self, source=source, target=target) for source, target in self.get_pairs()]

    def get_pairs(self):
        pairs = []
        for pos in self.nodes:
            pnode = self.nodes[pos]
            for npos in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                n = (pos[0] + npos[0], pos[1] + npos[1])
                if n in self.nodes:
                    nnode = self.nodes[n]
                    if nnode[2] > 0 and nnode[2] <= pnode[1] - pnode[2]:
                        pairs.append((nnode[0], pnode[0]))
        return pairs

    def get_pair_count_anywhere(self):
        cnt = 0
        for pnode in self.nodes.values():
            for nnode in self.nodes.values():
                if pnode[0] != nnode[0]:
                    if nnode[2] > 0 and nnode[2] <= pnode[1] - pnode[2]:
                        cnt +=1
        return cnt


def run_simulation(nh):
    buffer = [nh]
    visited = set()
    while len(buffer) > 0:
        print(len(buffer))
        print(buffer[0])
        n = buffer.pop(0)
        if n.goal == n.data:
            print(n)
            return n.steps
        else:
            for s in n.get_states():
                if s.get_hash() not in visited:
                    buffer.append(s)
                    visited.add(s.get_hash())


assert len(NodeHolder(lines=common.Loader.load_lines('test')).get_pairs()) == 6
assert NodeHolder(lines=common.Loader.load_lines('test')).get_pair_count_anywhere() == 25
print(f"Available pairs are {NodeHolder(lines=common.Loader.load_lines()).get_pair_count_anywhere()}")

assert run_simulation(NodeHolder(lines=common.Loader.load_lines('test_real'))) == 7
print([n for n in NodeHolder(lines=common.Loader.load_lines()).nodes.values() if n[2] == 0])
print(f"Available solution can be done in {run_simulation(NodeHolder(lines=common.Loader.load_lines()))} steps")