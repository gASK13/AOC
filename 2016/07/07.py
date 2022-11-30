import common
import re


def has_abba(part):
    for i in range(len(part) - 3):
        if part[i] == part[i + 3] and part[i + 1] == part[i + 2] and part[i] != part[i + 1]:
            return True
    return False


def get_abas(part, switch=False):
    abas = set()
    for i in range(len(part) - 2):
        if part[i] == part[i + 2] and part[i] != part[i + 1]:
            if switch:
                abas.add(part[i + 1] + part[i] + part[i + 1])
            else:
                abas.add(part[i:i + 3])
    return abas


def supports_tls(line):
    parts = re.split('[\\[\\]]', line)
    saw_abba = False
    for i in range(len(parts)):
        if i % 2 == 1 and has_abba(parts[i]):
            return False
        if i % 2 == 0 and has_abba(parts[i]):
            saw_abba = True
    return saw_abba


def supports_ssl(line):
    parts = re.split('[\\[\\]]', line)
    abas = set()
    for i in range(0, len(parts), 2):
        abas = abas.union(get_abas(parts[i], switch=True))
    for i in range(1, len(parts), 2):
        if len(abas.intersection(get_abas(parts[i]))) > 0:
            return True
    return False


assert has_abba('abba')
assert has_abba('ghabba')
assert has_abba('ghowllwghoooosl')
assert has_abba('habballao')
assert not has_abba('houwldka')
assert not has_abba('aaaaaaa')
assert not has_abba('howlaaalwoh')

assert supports_tls('abba[mnop]qrst')
assert not supports_tls('abcd[bddb]xyyx')
assert not supports_tls('aaaa[qwer]tyui')
assert supports_tls('ioxxoj[asdfgh]zxcvbn')

assert supports_tls('abcdefg[asdfgh]zxcvbn[abcdefg]oxxolol')
assert not supports_tls('abcdefg[asdfgh]zxcvbn[abcdefg]oxxolol[ohho]lowly')

assert supports_ssl('aba[bab]xyz')
assert not supports_ssl('xyx[xyx]xyx')
assert supports_ssl('aaa[kek]eke')
assert supports_ssl('zazbz[bzb]cdb')
assert supports_ssl('xyx[xyx]xyx[yxy]lol')

print(f'Lines that support TLS count = {sum([supports_tls(line) for line in common.Loader.load_lines()])}')

print(f'Lines that support SSL count = {sum([supports_ssl(line) for line in common.Loader.load_lines()])}')
