import common


class Program:
    def __init__(self, line):
        parts = line.split(' -> ')
        self.name = parts[0].split(' ')[0]
        self.val = int(parts[0].split(' ')[1][1:-1])
        self.children = []
        if len(parts) > 1:
            self.children_names = parts[1].split(', ')
        else:
            self.children_names = []

    def replace_child(self, child):
        if child.name in self.children_names:
            self.children_names.remove(child.name)
            self.children.append(child)
            return True
        return False

    def has_children(self):
        return len(self.children_names) > 0

    def weight(self):
        return self.val + sum([ch.weight() for ch in self.children])

    def balance(self, diff=0):
        weight_map = {}
        for ch in self.children:
            if ch.weight() not in weight_map:
                weight_map[ch.weight()] = []
            weight_map[ch.weight()].append(ch)
        if len(weight_map) == 1:
            return self.val + diff
        correct_weight = next(p for p in weight_map if len(weight_map[p]) > 1)
        wrong_weight = next(p for p in weight_map if len(weight_map[p]) == 1)
        return weight_map[wrong_weight][0].balance(correct_weight - wrong_weight)


def build_tree(_programs):
    while len(_programs) > 1:
        program = next(p for p in _programs if not p.has_children())
        _programs.remove(program)
        for p in _programs:
            p.replace_child(program)
    return _programs[0]


te = build_tree(common.Loader.transform_lines(Program, 'sample.txt'))
tr = build_tree(common.Loader.transform_lines(Program))
print('Example: {}'.format(te.name))
print('Real: {}'.format(tr.name))
print('Example wt: {}'.format(te.balance()))
print('Real wt: {}'.format(tr.balance()))
