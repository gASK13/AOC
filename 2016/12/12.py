import common

class Assembunny:
    def __init__(self, c=0):
        self.registers = {'c': c}

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
                        ptr += int(line[2]) - 1
            ptr += 1
        return self.registers['a']

    def get_register(self, ltr):
        if ltr not in self.registers:
            self.registers[ltr] = 0
        return self.registers[ltr]

    def get_value(self, item):
        if item.isnumeric():
            return int(item)
        else:
            return self.get_register(item)


assert Assembunny().run_code(common.Loader.load_lines('test')) == 42
print(f'Value of register A at end of code is {Assembunny().run_code(common.Loader.load_lines())}')

print(f'Value of register A with C=1 at end of code is {Assembunny(1).run_code(common.Loader.load_lines())}')
