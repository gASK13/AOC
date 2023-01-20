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
                case 'out':
                    print(self.get_value(line[1]))
                case 'cpy':
                    self.registers[line[2]] = self.get_value(line[1])
                case 'inc':
                    self.registers[line[1]] = self.get_register(line[1]) + 1
                case 'dec':
                    self.registers[line[1]] = self.get_register(line[1]) - 1
                case 'jnz':
                    if self.get_value(line[1]) != 0:
                        ptr += self.get_value(line[2]) - 1
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

# Found by reverse engineering the code in input and finding it outputs binary representation of A + certain constant (in reverse)
# Then it was just matter of computing 101010101010 - constant in binary and voila! 198!
Assembunny(a=198).run_code(common.Loader.load_lines())
