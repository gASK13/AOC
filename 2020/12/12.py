def apply(position, instruction, count):
    moves = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
    if instruction in moves:
        for i in range(0, count):
            position[0] += moves[instruction][0]
            position[1] += moves[instruction][1]
    elif instruction == 'F':
        for i in range(0, count):
            position[0] += position[2][0]
            position[1] += position[2][1]
    else:
        for i in range(0, count, 90):
            if instruction == 'R':
                position[2] = (-position[2][1], position[2][0])
            else:
                position[2] = (position[2][1], -position[2][0])


def apply_waypoint(_waypoint, instruction, count):
    print(_waypoint)
    moves = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
    if instruction in moves:
        _waypoint[2] = (_waypoint[2][0] + moves[instruction][0] * count, _waypoint[2][1] + moves[instruction][1] * count)
    elif instruction == 'F':
        _waypoint[0] += _waypoint[2][0] * count
        _waypoint[1] += _waypoint[2][1] * count
    else:
        for i in range(0, count, 90):
            if instruction == 'R':
                _waypoint[2] = (-_waypoint[2][1], _waypoint[2][0])
            else:
                _waypoint[2] = (_waypoint[2][1], -_waypoint[2][0])


# PART ONE + TWO
position = [0, 0, (1, 0)]
waypoint_position = [0, 0, (10, -1)]
for line in open('12.txt').readlines():
    line = line.strip()
    apply(position, line[0], int(line[1:]))
    apply_waypoint(waypoint_position, line[0], int(line[1:]))

print('PART ONE ENDED AT {} WITH DISTANCE {}'.format(position, abs(position[0]) + abs(position[1])))
print('PART TWO ENDED AT {} WITH DISTANCE {}'.format(waypoint_position, abs(waypoint_position[0]) + abs(waypoint_position[1])))


