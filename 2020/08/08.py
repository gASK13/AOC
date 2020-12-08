class Stack:
    def __init__(self, ptr, acc):
        self.ptr = ptr
        self.acc = acc
        self.step = 1

class Instruction:
    def __init__(self, line):
        self.operation = line.split(' ')[0]
        self.value = int(line.split(' ')[1])
        self.visited = None

    def run(self, stack):
        self.visited = stack.step
        stack.step += 1
        if self.operation == 'acc':
            stack.acc += self.value
        if self.operation == 'jmp':
            stack.ptr += self.value
        else:
            stack.ptr += 1

    def __str__(self):
        return '{} {}   \t| {}'.format(self.operation, self.value, self.visited if self.visited is not None else '')


def runProgram(program, state):
    for line in program:
        line.visited = None
    while True:
        if state.ptr > len(program):
            return False
        if state.ptr == len(program):
            return True
        if program[state.ptr].visited is not None:
            return False
        program[state.ptr].run(state)


def switchOperaion(instruction):
    if instruction.operation == 'nop':
        instruction.operation = 'jmp'
    elif instruction.operation == 'jmp':
        instruction.operation = 'nop'


def printProgram(program):
    for line in program:
        print(str(line))


instructions = []
for line in open('08.txt', 'r').readlines():
    instructions.append(Instruction(line))

# PART ONE
stack = Stack(0, 0)
runProgram(instructions, stack)
print(stack.acc)

# PART TWO
for instruction in instructions:
    stack = Stack(0, 0)
    switchOperaion(instruction)
    #print('------------------')
    #printProgram(instructions)
    if runProgram(instructions, stack):
        print("RETURNED FINE WITH {} IN ACC".format(stack.acc))
    switchOperaion(instruction)
