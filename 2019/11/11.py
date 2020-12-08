import math
import csv
from itertools import permutations

scr = {}


def getInput():
    # get color of field I am over
    return scr[str(robot[0]) + '#' + str(robot[1])][0]


def digit(n, d):
    return math.floor((n % math.pow(10, d) / math.pow(10, d - 1)))


def parameter(arr, pos, i, base):
    if digit(arr[pos], i + 2) == 1:
        return arr[pos + i]
    elif digit(arr[pos], i + 2) == 2:
        return arr[arr[pos + i] + base]
    else:
        return arr[arr[pos + i]]


def setVal(arr, pos, i, base, val):
    if digit(arr[pos], i + 2) == 2:
        arr[arr[pos + i] + base] = val
    else:
        arr[arr[pos + i]] = val


def op(pos, arr, output, base):
    if (arr[pos] % 10 == 1):
        a = parameter(arr, pos, 1, base[0])
        b = parameter(arr, pos, 2, base[0])
        setVal(arr, pos, 3, base[0], a + b)
        return pos + 4
    elif (arr[pos] % 10 == 2):
        a = parameter(arr, pos, 1, base[0])
        b = parameter(arr, pos, 2, base[0])
        setVal(arr, pos, 3, base[0], a * b)
        return pos + 4
    elif (arr[pos] % 10 == 3):
        setVal(arr, pos, 1, base[0], getInput())
        return pos + 2
    elif (arr[pos] % 10 == 4):
        a = parameter(arr, pos, 1, base[0])
        output.append(a)
        return pos + 2
    elif (arr[pos] % 10 == 5):
        a = parameter(arr, pos, 1, base[0])
        b = parameter(arr, pos, 2, base[0])
        if a != 0:
            return b
        return pos + 3
    elif (arr[pos] % 10 == 6):
        a = parameter(arr, pos, 1, base[0])
        b = parameter(arr, pos, 2, base[0])
        if a == 0:
            return b
        return pos + 3
    elif (arr[pos] % 10 == 7):
        a = parameter(arr, pos, 1, base[0])
        b = parameter(arr, pos, 2, base[0])
        if a < b:
            setVal(arr, pos, 3, base[0], 1)
        else:
            setVal(arr, pos, 3, base[0], 0)
        return pos + 4
    elif (arr[pos] % 10 == 8):
        a = parameter(arr, pos, 1, base[0])
        b = parameter(arr, pos, 2, base[0])
        if a == b:
            setVal(arr, pos, 3, base[0], 1)
        else:
            setVal(arr, pos, 3, base[0], 0)
        return pos + 4
    elif (arr[pos] % 10 == 9):
        a = parameter(arr, pos, 1, base[0])
        base[0] += a
        return pos + 2


def run(row, pos, input, base):
    i = pos
    output = []
    step_count = 0
    while i < len(row):
        if (row[i] == 99):
            return {'halt': True, 'output': output, 'step_count': step_count}
        i = op(i, row, output, base)
        if len(output) == 2:
            print(output)
            if scr[str(robot[0]) + '#' + str(robot[1])][0] != output[0]:
                if not scr[str(robot[0]) + '#' + str(robot[1])][1]:
                    step_count += 1
                scr[str(robot[0]) + '#' + str(robot[1])][0] = output[0]
                scr[str(robot[0]) + '#' + str(robot[1])][1] = True
            turnRobot(output[1])
            moveRobot()
            output = []

def moveRobot():
    if robot[2] == 'up':
        robot[0] = robot[0] - 1
    elif robot[2] == 'left':
        robot[1] = robot[1] - 1
    elif robot[2] == 'down':
        robot[0] = robot[0] + 1
    elif robot[2] == 'right':
        robot[1] = robot[1] + 1
    if str(robot[0]) + '#' + str(robot[1]) not in scr:
        scr[str(robot[0]) + '#' + str(robot[1])] = [0, False]

def turnRobot(dir):
    if dir == 0:
        if robot[2] == 'up':
            robot[2] = 'left'
        elif robot[2] == 'left':
            robot[2] = 'down'
        elif robot[2] == 'down':
            robot[2] = 'right'
        elif robot[2] == 'right':
            robot[2] = 'up'
    else:
        if robot[2] == 'down':
            robot[2] = 'left'
        elif robot[2] == 'right':
            robot[2] = 'down'
        elif robot[2] == 'up':
            robot[2] = 'right'
        elif robot[2] == 'left':
            robot[2] = 'up'

def loadRow():
    roww = []
    with open('11.txt', 'r') as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for rw in reader:
            roww = rw

    i = 0
    while i < len(roww):
        roww[i] = int(roww[i])
        i += 1
    for i in range(0, 100000):
        roww.append(0);
    return roww


scr['0#0'] = [1, False]
robot = [0, 0, 'up']

out = run(loadRow(), 0, [], [0])
print(out)

for y in range(0, 6):
    line = ''
    for x in range(0, 43):
        if str(y) + '#' + str(x) in scr:
            line += 'X' if scr[str(y) + '#' + str(x)][0] == 1 else ' '
        else:
            line += ' '
    print(line)

#0-5
#0-42







