import math
import csv
import random

def digit(n, d):
    return math.floor((n % math.pow(10, d) / math.pow(10, d - 1)))

def printMap(mat):
    for line in mat:
        print(''.join([item for item in line]))

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

def loadRow():
    roww = []
    with open('15.txt', 'r') as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for rw in reader:
            roww = rw

    i = 0
    while i < len(roww):
        roww[i] = int(roww[i])
        i += 1
    for i in range(0, 10000):
        roww.append(0);
    return roww

def buildMap(w):
    map = []
    for i in range(0, 2*w):
        map.append([])
        for j in range(0, 2*w):
            map[i].append(' ')
    return map

w = 25
map = buildMap(w)
printMap(map)
robot = [w, w, 1, [(w, w-1)], False]
oxygen = [0,0]


def run(row, pos, base):
    i = pos
    output = []
    while i < len(row):
        if (row[i] == 99):
            return {'halt': True, 'output': output};
        i = op(i, row, output, base)
        if len(output) == 1:
            process(output[0])
            output = []
        if robot[4]:
            return

def process(output):
    if output == 2:
        setNextCell(robot, 'o')
        updateRobot(robot)
        oxygen[0] = robot[0]
        oxygen[1] = robot[1]
    if output == 1:
        if getNextCell(robot) == ' ':
            setNextCell(robot, '.')
        updateRobot(robot)
    if output == 0:
        setNextCell(robot, '#')

def getNextCell(robot):
    mv = robot[2]
    if mv == 1:
        return map[robot[1] - 1][robot[0]]
    if mv == 2:
        return map[robot[1] + 1][robot[0]]
    if mv == 3:
        return map[robot[1]][robot[0] - 1]
    if mv == 4:
        return map[robot[1]][robot[0] + 1]

def setNextCell(robot, value):
    mv = robot[2]
    if mv == 1:
        map[robot[1] - 1][robot[0]] = value
    if mv == 2:
        map[robot[1] + 1][robot[0]] = value
    if mv == 3:
        map[robot[1]][robot[0] - 1] = value
    if mv == 4:
        map[robot[1]][robot[0] + 1] = value

def updateRobot(robot):
    mv = robot[2]
    if mv == 1:
        robot[1] = robot[1] - 1
    if mv == 2:
        robot[1] = robot[1] + 1
    if mv == 3:
        robot[0] = robot[0] - 1
    if mv == 4:
        robot[0] = robot[0] + 1

def translate_direction(dir):
    if robot[0] == dir[0]:
        if robot[1] + 1 == dir[1]:
            return 2
        else:
            return 1
    else:
        if robot[0] + 1 == dir[0]:
            return 4
        else:
            return 3

def computePath(x, y, char):
    stack = [[(x + 1, y)], [(x, y + 1)], [(x, y - 1)], [(x - 1, y)]]
    while len(stack) > 0:
        st = stack.pop(0)
        if map[st[-1][1]][st[-1][0]] == char:
            return st
        if map[st[-1][1]][st[-1][0]] == '.':
            if (st[-1][0] + 1, st[-1][1]) not in st:
                stack.append(st + [(st[-1][0] + 1, st[-1][1])])
            if (st[-1][0] - 1, st[-1][1]) not in st:
                stack.append(st + [(st[-1][0] - 1, st[-1][1])])
            if (st[-1][0], st[-1][1] + 1) not in st:
                stack.append(st + [(st[-1][0], st[-1][1] + 1)])
            if (st[-1][0], st[-1][1] - 1) not in st:
                stack.append(st + [(st[-1][0], st[-1][1] - 1)])

    robot[4] = True
    return [(x + 1, y)]

def fillMap(x, y):
    map[y][x] = 'O'
    timer = -1
    next_stack = [(x, y)]
    while len(next_stack) > 0:
        timer += 1
        stack = next_stack
        next_stack = []
        while len(stack) > 0:
            st = stack.pop(0)
            map[st[1]][st[0]] = 'O'
            if map[st[1] + 1][st[0]] == '.':
                next_stack.append((st[0], st[1] + 1))
            if map[st[1] - 1][st[0]] == '.':
                next_stack.append((st[0], st[1] - 1))
            if map[st[1]][st[0] + 1] == '.':
                next_stack.append((st[0] + 1, st[1]))
            if map[st[1]][st[0] - 1] == '.':
                next_stack.append((st[0] - 1, st[1]))

    return timer

def getInput():
    if len(robot[3]) == 0:
        robot[3] = computePath(robot[0], robot[1], ' ')
    robot[2] = translate_direction(robot[3].pop(0))
    return robot[2]

# ONE
run(loadRow(), 0, [0])
printMap(map)
pth = computePath(w, w, 'o')
print(len(pth))
print(pth)

# TWO
print(fillMap(oxygen[0], oxygen[1]))






