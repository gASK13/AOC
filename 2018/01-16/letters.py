def reactLength(line):
    ln = len(line)
    while True:
        for ltr in string.ascii_lowercase:
            line = line.replace(ltr + ltr.upper(), '')
            line = line.replace(ltr.upper() + ltr, '')
        if (len(line) == ln):
            break
        ln = len(line)
    return len(line)

      

import string

minln = 100000
minltr = '0'
for ltr in string.ascii_lowercase:
    ln = reactLength(open('input.txt', 'r').readlines()[0].rstrip().replace(ltr, '').replace(ltr.upper(), ''))
    if (ln < minln):
        minln = ln
        minltr = ltr

print(minln)
print(minltr)