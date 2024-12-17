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

def part_two(lines):
    a, b, c, program = parse_lines(lines)
    with open('plant.out', 'w') as the_file:
        max = 100000000
        for i in tqdm(range(max)):
            t = TriBit(i, b, c, program)
            t.run()
            the_file.write(f'{i:09d} >> {t.output}\r\n')
            if t.output == program:
                return i
    raise Exception(f"Not found in {max} iterations!")


def parse_lines(lines):
    a = int(lines.pop(0).split(': ')[1])
    b = int(lines.pop(0).split(': ')[1])
    c = int(lines.pop(0).split(': ')[1])
    lines.pop(0)
    program = [int(_) for _ in lines.pop(0)[9:].split(',')]
    return a, b, c, program


assert part_one(common.Loader.load_lines('test')) == '4,6,3,5,6,3,5,2,1,0'
print(f'Part 1:{Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Fore.RESET}{Back.RESET}')

assert part_two(common.Loader.load_lines('test_2')) == 117440
print(f'Part 2:{Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines())}{Fore.RESET}{Back.RESET}')