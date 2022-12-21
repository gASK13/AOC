import common
import hashlib

def find_key(prefix, find):
    i = 0
    while True:
        hsh = hashlib.md5(f'{prefix}{i}'.encode('utf-8')).hexdigest()
        if hsh.startswith(find):
            return i
        i += 1

test_data = {'abcdef': 609043, 'pqrstuv': 1048970}
for t in test_data:
    assert find_key(t, '00000') == test_data[t]

print(f'Real answer is {find_key(common.Loader.load_lines()[0], "00000")}')
print(f'Real answer for 000000 is {find_key(common.Loader.load_lines()[0], "000000")}')