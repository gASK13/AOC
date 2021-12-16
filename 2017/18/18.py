import common


class Instruction:
    def __init__(self, line):
        split = line.split(' ')
        self.op = split[0]
        self.reg = split[1]
        self.param = None
        self.value = None
        if len(split) > 2:
            try:
                self.value = int(split[2])
            except:
                self.param = split[2]

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
    def __init__(self, program, p):
        self.ptr = 0
        self.queue = []
        self.id = p
        self.mem = Memory()
        self.mem.set_value('p', p)
        self.program = program
        self.waiting = False
        self.terminated = False
        self.send_count = 0
        self.step_count = 0

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
            case 'mul':
                self.mem.set_value(instruction.reg, self.mem.get_value(instruction.reg) * instruction.get_value(self.mem))
            case 'mod':
                self.mem.set_value(instruction.reg, self.mem.get_value(instruction.reg) % instruction.get_value(self.mem))
            case 'rcv':
                if len(self.queue) == 0:
                    self.waiting = True
                    return
                self.mem.set_value(instruction.reg, self.queue.pop())
            case 'jgz':
                if self.mem.get_value(instruction.reg) > 0:
                    self.ptr -= 1
                    self.ptr += instruction.get_value(self.mem)
        self.ptr += 1
        return


def run_program(_prgrm):
    program = Program(_prgrm, 0)
    snd = 0
    while True:
        value = program.step()
        if value is not None:
            snd = value
        if program.waiting:
            if program.mem.get_value(program.program[program.ptr].reg) == 0:
                program.receive(0)
            else:
                return snd


def run_two_programs(_prgrm):
    program0 = Program(_prgrm, 0)
    program1 = Program(_prgrm, 1)
    while True:
        program0.receive(program1.step())
        program1.receive(program0.step())
        if program0.waiting and program1.waiting:
            print("DEADLOCK")
            return program1.send_count
        if program0.terminated and program1.terminated:
            print("TERMINATED")
            return program1.send_count
        #print(f'Step counts {program0.step_count} / {program1.step_count}')
        #print(f'Send counts {program0.send_count} / {program1.send_count}')
        #print(f'Ptr {program0.ptr} / {program1.ptr}')
        #print(f'Queue lengths {len(program0.queue)} / {len(program1.queue)}')


print(f'Test = {run_program(common.Loader.transform_lines(Instruction, "test.txt"))} (expected 4)')
print(f'Real = {run_program(common.Loader.transform_lines(Instruction))}')

print(f'Test = {run_two_programs(common.Loader.transform_lines(Instruction, "test_parallel.txt"))}')
print(f'Test = {run_two_programs(common.Loader.transform_lines(Instruction))}')