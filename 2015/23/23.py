import common
from colorama import Fore, Back, Style

class LittleMarieFirstComputer:
    def __init__(self, lines, a=0):
        self.registers = {'a': a, 'b': 0}
        self.instructions = lines
        self.pointer = 0

    def run(self):
        while self.pointer < len(self.instructions):
            self.execute(self.instructions[self.pointer])
        return self.registers

    def execute(self, instruction):
        match instruction[0:3]:
            case 'hlf':
                self.registers[instruction[4]] //= 2
            case 'tpl':
                self.registers[instruction[4]] *= 3
            case 'inc':
                self.registers[instruction[4]] += 1
            case 'jmp':
                self.pointer += int(instruction[4:])
                return
            case 'jie':
                if self.registers[instruction[4]] % 2 == 0:
                    self.pointer += int(instruction[7:])
                    return
            case 'jio':
                if self.registers[instruction[4]] == 1:
                    self.pointer += int(instruction[7:])
                    return
        self.pointer += 1


assert LittleMarieFirstComputer(common.Loader.load_lines('test')).run()['a'] == 2

print(f'Part 1: {Fore.BLACK}{Back.GREEN}{LittleMarieFirstComputer(common.Loader.load_lines()).run()["b"]}')

print(f'Part 2: {Fore.BLACK}{Back.GREEN}{LittleMarieFirstComputer(common.Loader.load_lines(), 1).run()["b"]}')

