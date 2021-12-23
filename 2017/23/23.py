import common


class Instruction:
    def __init__(self, line):
        split = line.split(' ')
        self.op = split[0]
        try:
            self.reg = None
            self.reg_val = int(split[1])
        except:
            self.reg = split[1]
            self.reg_val = None
        self.param = None
        self.value = None
        if len(split) > 2:
            try:
                self.value = int(split[2])
            except:
                self.param = split[2]

    def get_reg_value(self, mem):
        if self.reg_val is not None:
            return self.reg_val
        if self.reg is not None:
            return mem.get_value(self.reg)

    def get_value(self, mem):
        if self.value is not None:
            return self.value
        if self.param is not None:
            return mem.get_value(self.param)


class Memory:
    def __init__(self):
        self.mem = {}

    def get_value(self, letter):
        if letter not in self.mem:
            self.mem[letter] = 0
        return self.mem[letter]

    def set_value(self, letter, value):
        self.mem[letter] = value


class Program:
    def __init__(self, program, part_two=False):
        self.ptr = 0
        self.queue = []
        self.mem = Memory()
        self.mem.set_value('a', 1 if part_two else 0)
        self.program = program
        self.waiting = False
        self.terminated = False
        self.send_count = 0
        self.step_count = 0
        self.mul_count = 0

    def receive(self, value):
        if value is None:
            return

        if self.waiting:
            self.waiting = False
            instruction = self.program[self.ptr]
            self.mem.set_value(instruction.reg, value)
            self.ptr += 1
        else:
            self.queue.append(value)

    def step(self):
        if self.waiting:
            return

        if 0 > self.ptr or self.ptr >= len(self.program):
            self.terminated = True
            return

        instruction = self.program[self.ptr]
        self.step_count += 1
        match instruction.op:
            case 'snd':
                self.ptr += 1
                self.send_count += 1
                return self.mem.get_value(instruction.reg)
            case 'set':
                self.mem.set_value(instruction.reg, instruction.get_value(self.mem))
            case 'add':
                self.mem.set_value(instruction.reg, self.mem.get_value(instruction.reg) + instruction.get_value(self.mem))
            case 'sub':
                self.mem.set_value(instruction.reg, self.mem.get_value(instruction.reg) - instruction.get_value(self.mem))
            case 'mul':
                self.mul_count += 1
                self.mem.set_value(instruction.reg, self.mem.get_value(instruction.reg) * instruction.get_value(self.mem))
            case 'mod':
                self.mem.set_value(instruction.reg, self.mem.get_value(instruction.reg) % instruction.get_value(self.mem))
            case 'rcv':
                if len(self.queue) == 0:
                    self.waiting = True
                    return
                self.mem.set_value(instruction.reg, self.queue.pop(0))
            case 'jgz':
                if instruction.get_reg_value(self.mem) > 0:
                    self.ptr -= 1
                    self.ptr += instruction.get_value(self.mem)
            case 'jnz':
                if instruction.get_reg_value(self.mem) != 0:
                    self.ptr -= 1
                    self.ptr += instruction.get_value(self.mem)
        self.ptr += 1
        return


def run_program(_prgrm, part_two=False):
    program = Program(_prgrm, part_two)
    it = 0
    while not program.terminated:
        program.step()
        it +=1
        print(program.mem.mem)
    return program.mul_count, program.mem.mem


print(f'Real = {run_program(common.Loader.transform_lines(Instruction))}')
print(f'Real pt 2 = {run_program(common.Loader.transform_lines(Instruction), part_two=True)}')
