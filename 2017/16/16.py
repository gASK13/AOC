import common
import time


def parse_steps(steps):
    final_steps = []
    for step in steps:
        match step[0]:
            case 's':
                final_steps.append(('s', int(step[1:])))
            case 'x':
                final_steps.append(('x', [int(x) for x in step[1:].split('/')]))
            case 'p':
                final_steps.append(('p', [x for x in step[1:].split('/')]))
    return final_steps


class DanceFloor:
    def __init__(self, order):
        self.order = [x for x in order]

    def swap(self, positions):
        tmp = self.order[positions[0]]
        self.order[positions[0]] = self.order[positions[1]]
        self.order[positions[1]] = tmp

    def dance(self, steps):
        for step, params in steps:
            self.step(step, params)

    def step(self, step, params):
        match step:
            case 's':
                self.order = self.order[-params:] + self.order[:-params]
            case 'x':
                self.swap(params)
            case 'p':
                positions = [self.order.index(x) for x in params]
                self.swap(positions)

    def __str__(self):
        return ''.join(self.order)


test_data = ['abcde', [('s', 1), ('x', [3, 4]), ('p', ['e', 'b'])], 'baedc', 'ceadb']
df = DanceFloor(test_data[0])
df.dance(test_data[1])
print(f'State = {df}, Expected = {test_data[2]}')
df.dance(test_data[1])
print(f'State = {df}, Expected = {test_data[3]}')

# REAL
df = DanceFloor('abcdefghijklmnop')
steps = parse_steps(common.Loader.load_matrix(delimiter=',')[0])
df.dance(steps)
print(f'Final state after one round {df}')

# ONE BILLION? NICE!
df = DanceFloor('abcdefghijklmnop')
seen = {str(df): 0}
seen_idx = [str(df)]
i = 0
while True:
    df.dance(steps)
    i += 1
    if str(df) not in seen:
        seen[str(df)] = i
        seen_idx.append(str(df))
    else:
        break
    if i % 1000 == 0:
        print(i)

print(f'Stopped at {i}, last seen at {seen[str(df)]}')
offset = seen[str(df)]
delta = i - seen[str(df)]
final_iterations = (1000000000 - offset) % delta
print(seen_idx[final_iterations])
