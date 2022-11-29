import common
import hashlib


def get_pass(prefix):
    idx = 0
    pwd = ''
    while True:
        hsh = hashlib.md5(f'{prefix}{idx}'.encode('utf-8')).hexdigest()
        if hsh[:5] == '00000':
            print(hsh)
            pwd = pwd + hsh[5]
        if len(pwd) == 8:
            print(pwd)
            return pwd
        idx += 1


def get_pass_hard(prefix):
    idx = 0
    found = 0
    pwd = ['_' for i in range(8)]
    while True:
        hsh = hashlib.md5(f'{prefix}{idx}'.encode('utf-8')).hexdigest()
        if hsh[:5] == '00000' and hsh[5] in ['0', '1', '2', '3', '4', '5', '6', '7'] and pwd[int(hsh[5])] == '_':
            print(hsh)
            pwd[int(hsh[5])] = hsh[6]
            found += 1
        if found == 8:
            print(''.join(pwd))
            return ''.join(pwd)
        idx += 1


assert get_pass('abc') == '18f47a30'
print(f'Password is {get_pass(common.Loader.load_lines()[0])}')

assert get_pass_hard('abc') == '05ace8e3'
print(f'Password is {get_pass_hard(common.Loader.load_lines()[0])}')
