import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intcode import Parostroj

class InputBuffer:
    def __init__(self):
        self.buffer = []

    def get_input(self):
        if len(self.buffer) == 0:
            self.prompt_user()
        return self.buffer.pop(0)

    def prompt_user(self):
        user_input = input()
        self.buffer = [ord(char) for char in user_input] + [10]


def print_output(output):
    print(chr(output), end='')


program = open('25.txt', 'r').readline()
input_buffer = InputBuffer()
Parostroj(program, output_processor=print_output, input_provider=input_buffer.get_input).run()