import math

class Parostroj:
    def __init__(self, program, input_provider=None, output_processor=None):
        self.program = [int(number) for number in program.strip().split(',')]
        self.input_provider = input_provider
        self.output_processor = output_processor if output_processor is not None else lambda x: self.output.append(x)
        self.output = None if output_processor is not None else []
        self.base = 0

    def pad_program(self, length):
        if length >= len(self.program):
            self.program = self.program + [0 for i in range(len(self.program), length + 1)]

    def safe_get(self, pos):
        self.pad_program(pos)
        return self.program[pos]

    def safe_set(self, pos, value):
        self.pad_program(pos)
        self.program[pos] = value

    def run(self, input_array=None, stop_check=None):
        if input_array is not None:
            self.input_provider = lambda: input_array.pop(0)

        pos = 0
        while True:
            if self.safe_get(pos) == 99:
                return self.output
            pos = self.instruction(pos)
            if stop_check is not None:
                if stop_check():
                    return self.output


    @staticmethod
    def digit(n, d):
        return math.floor((n % math.pow(10, d) / math.pow(10, d - 1)))

    def parameter(self, pos, arg):
        mode = self.digit(self.safe_get(pos), arg + 2)
        if mode == 1:
            return self.safe_get(pos + arg)
        elif mode == 2:
            return self.safe_get(self.safe_get(pos + arg) + self.base)
        else:
            return self.safe_get(self.safe_get(pos + arg))

    def set_val(self, pos, arg, value):
        if self.digit(self.safe_get(pos), arg + 2) == 2:
            self.safe_set(self.safe_get(pos + arg) + self.base, value)
        else:
            self.safe_set(self.safe_get(pos + arg), value)

    def instruction(self, pos):
        op_code = self.safe_get(pos) % 10
        if op_code == 1:
            self.set_val(pos, 3, self.parameter(pos, 1) + self.parameter(pos, 2))
            return pos + 4
        elif op_code == 2:
            self.set_val(pos, 3, self.parameter(pos, 1) * self.parameter(pos, 2))
            return pos + 4
        elif op_code == 3:
            self.set_val(pos, 1, self.input_provider())
            return pos + 2
        elif op_code == 4:
            self.output_processor(self.parameter(pos, 1))
            return pos + 2
        elif op_code == 5:
            if self.parameter(pos, 1) != 0:
                return self.parameter(pos, 2)
            return pos + 3
        elif op_code == 6:
            if self.parameter(pos, 1) == 0:
                return self.parameter(pos, 2)
            return pos + 3
        elif op_code == 7:
            if self.parameter(pos, 1) < self.parameter(pos, 2):
                self.set_val(pos, 3, 1)
            else:
                self.set_val(pos, 3, 0)
            return pos + 4
        elif op_code == 8:
            if self.parameter(pos, 1) == self.parameter(pos, 2):
                self.set_val(pos, 3, 1)
            else:
                self.set_val(pos, 3, 0)
            return pos + 4
        elif op_code == 9:
            self.base += self.parameter(pos, 1)
            return pos + 2

print(Parostroj('109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99').run())
