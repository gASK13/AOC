tape = set()


def get_tape(idx):
    return 1 if idx in tape else 0


def set_tape(idx, value):
    if value == 1:
        tape.add(idx)
    elif idx in tape:
        tape.remove(idx)


states = {
    'a': {0: (1, 1, 'b'), 1: (0, 1, 'f')},
    'b': {0: (0, -1, 'b'), 1: (1, -1, 'c')},
    'c': {0: (1, -1, 'd'), 1: (0, 1, 'c')},
    'd': {0: (1, -1, 'e'), 1: (1, 1, 'a')},
    'e': {0: (1, -1, 'f'), 1: (0, -1, 'd')},
    'f': {0: (1, 1, 'a'), 1: (0, -1, 'e')}
}

state = 'a'
idx = 0
for i in range(12425180):
    value, step, state = states[state][get_tape(idx)]
    set_tape(idx, value)
    idx += step

print(len(tape))