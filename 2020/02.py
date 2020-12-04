def validatePass(line):
    lower = int(line.split('-')[0])
    upper = int(line.split('-')[1].split(' ')[0])
    char = line.split(' ')[1].split(':')[0]
    pwd = line.split(':')[1].lstrip()
    return (pwd[lower - 1] == char) ^ (pwd[upper - 1] == char)


valid = 0
for line in open('02.txt', 'r').readlines():
    if validatePass(line):
        valid = valid + 1

print(valid)

