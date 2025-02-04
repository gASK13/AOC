import common
from colorama import Fore, Back
import math
from tqdm import tqdm

class TriBit:
    def __init__(self, a, b, c, program):
        self.registers = {}
        self.registers['A'] = a
        self.registers['B'] = b
        self.registers['C'] = c
        self.output = []
        self.program = program
        self.ptr = 0

    def get_value(self, operand):
        match operand:
            case 0:
                return operand
            case 1:
                return operand
            case 2:
                return operand
            case 3:
                return operand
            case 4:
                return self.registers['A']
            case 5:
                return self.registers['B']
            case 6:
                return self.registers['C']
            case 7:
                raise Exception('OUCH!')

    def run(self):
        while self.ptr < len(self.program):
            self._step(self.program[self.ptr], self.program[self.ptr + 1])

    def _step(self, instruction, operand):
        match instruction:
            case 0:
                self.registers['A'] = math.trunc(self.registers['A'] / pow(2, self.get_value(operand)))
            case 1:
                self.registers['B'] = self.registers['B'] ^ operand
            case 2:
                self.registers['B'] = self.get_value(operand) % 8
            case 3:
                if self.registers['A'] != 0:
                    self.ptr = operand
                    return
            case 4:
                self.registers['B'] = self.registers['B'] ^ self.registers['C']
            case 5:
                self.output.append(self.get_value(operand) % 8)
            case 6:
                self.registers['B'] = math.trunc(self.registers['A'] / pow(2, self.get_value(operand)))
            case 7:
                self.registers['C'] = math.trunc(self.registers['A'] / pow(2, self.get_value(operand)))
        self.ptr += 2

    def get_output(self):
        return ','.join([str(n) for n in self.output])

    def __str__(self):
        return str(self.registers)

    def __repr__(self):
        return str(self)

def part_one(lines):
    a, b, c, program = parse_lines(lines)

    t = TriBit(a, b, c, program)
    t.run()

    return t.get_output()


def run_test(i, out):
    a = i
    ptr = 0
    while True:
        b = (a % 8) ^ 5
        c = math.trunc(a / pow(2,b))
        b = b ^ 6
        a = math.trunc(a / 8)
        b = b ^ c
        if b % 8 != out[ptr] or ptr > len(out):
            return False
        ptr += 1
        if a == 0:
            return ptr > len(out)

def run_one(i):
    a = i
    b = (a % 8) ^ 5
    c = math.trunc(a / pow(2,b))
    b = b ^ 6
    b = b ^ c
    return b % 8


def part_two(lines):
    # 2,4,1,5,7,5,1,6,0,3,4,6,5,5,3,0
    # OK, so output "tail' is based solely on A!!! (b and C are overwritten)
    # so we can go from "end" and find all values that produce tail and then add next number (multiply by 8 and add up to 8)!
    a, b, c, program = parse_lines(lines)

    # find all As that produce the "tail"
    # must be 0-7
    solutions = [0]
    while len(program) > 0:
        options = [_ * 8 for _ in solutions]
        solutions = []
        next = program.pop()
        for o in options:
            for i in range(o, o+8):
                if run_one(i) == next:
                    solutions.append(i)
        print(f'For {next} found {solutions} as options.')
    return min(solutions)

def parse_lines(lines):
    a = int(lines.pop(0).split(': ')[1])
    b = int(lines.pop(0).split(': ')[1])
    c = int(lines.pop(0).split(': ')[1])
    lines.pop(0)
    program = [int(_) for _ in lines.pop(0)[9:].split(',')]
    return a, b, c, program


assert part_one(common.Loader.load_lines('test')) == '4,6,3,5,6,3,5,2,1,0'
print(f'Part 1:{Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Fore.RESET}{Back.RESET}')

print(f'Part 2:{Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines())}{Fore.RESET}{Back.RESET}')





