import common
from collections import Counter


def decode_simple(message, last=False):
    message = [[message[j][i] for j in range(len(message))] for i in range(len(message[0]))]
    return ''.join([Counter(charline).most_common()[-1 if last else 0][0] for charline in message])

assert decode_simple(common.Loader.load_lines('test.txt')) == 'easter'
print(f'The secret message is {decode_simple(common.Loader.load_lines())}')

assert decode_simple(common.Loader.load_lines('test.txt'), True) == 'advent'
print(f'The secret message (least common) is {decode_simple(common.Loader.load_lines(), True)}')
