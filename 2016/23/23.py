import common
import math

class Assembunny:
    def __init__(self, a=0):
        self.registers = {'a': a}

    def run_code(self, code):
        ptr = 0
        while ptr < len(code):
            line = code[ptr].split(' ')
            match line[0]:
                case 'cpy':
                    self.registers[line[2]] = self.get_value(line[1])
                case 'inc':
                    self.registers[line[1]] = self.get_register(line[1]) + 1
                case 'dec':
                    self.registers[line[1]] = self.get_register(line[1]) - 1
                case 'jnz':
                    if self.get_value(line[1]) != 0:
                        ptr += self.get_value(line[2]) - 1
                case 'tgl':
                    where = self.get_value(line[1]) + ptr
                    if 0 <= where < len(code):
                        match code[where].split(' ')[0]:
                            case 'cpy':
                                code[where] = code[where].replace('cpy', 'jnz')
                            case 'inc':
                                code[where] = code[where].replace('inc', 'dec')
                            case 'dec':
                                code[where] = code[where].replace('dec', 'inc')
                            case 'jnz':
                                code[where] = code[where].replace('jnz', 'cpy')
                            case 'tgl':
                                code[where] = code[where].replace('tgl', 'inc')
            ptr += 1
        return self.registers['a']

    def get_register(self, ltr):
        if ltr not in self.registers:
            self.registers[ltr] = 0
        return self.registers[ltr]

    def get_value(self, item):
        if item.isnumeric() or (item[0] == '-' and item[1:].isnumeric()):
            return int(item)
        else:
            return self.get_register(item)


assert Assembunny().run_code(common.Loader.load_lines('test_s')) == 3
print(f'Value of register A at end of code is {Assembunny(a=7).run_code(common.Loader.load_lines())}')

#print(f'Value of register A at end of code with proper egg count is {Assembunny(a=12).run_code(common.Loader.load_lines())}')
# I reverse engineered the code, duh!
assert math.factorial(7) + 77*99 == 12663
print(math.factorial(12) + 77*99)
