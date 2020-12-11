import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intcode import Parostroj


def print_output(_output):
    for char in _output:
        if char > 128:
            print('RESULT {}'.format(char))
        else:
            print(chr(char), end='')


def translate_program(_prog):
    input = []
    for line in _prog:
        for char in line:
            input.append(ord(char))
        input.append(10)
    return input

# PARTO ONE
input = ['NOT A J', 'NOT B T', 'OR T J', 'NOT C T', 'OR T J', 'AND D J', 'WALK']
output = Parostroj(open('21.txt', 'r').readline()).run(input_array=translate_program(input))
print_output(output)

# PARTO TWO
input = ['NOT G J', 'AND H J', 'NOT F T', 'OR T J', 'OR E J', 'NOT C T', 'AND T J', 'NOT B T', 'OR T J', 'NOT A T', 'OR T J', 'AND D J', 'RUN']
output = Parostroj(open('21.txt', 'r').readline()).run(input_array=translate_program(input))
print_output(output)

# HERE IS THE LOGIC, MADE BY HAND
# D == 1
# and
# (A == 0 or B == 0 or (c == 0 and (f == 0 OR e == 1 or (g == 0 and h == 1))

#1111 - DONT
#11010100 - DONT
#11010101 - OD
#110100 - DO
#11011 - DO
#1011 - JUMP
#1001 - JUMP
#0101 - JUMP
#0001 - JUMP


