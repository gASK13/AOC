entries = []
doubles = []
for line in open('01.txt', 'r').readlines():
    nEntry = int(line)
    for double in doubles:
        if double['sum'] + nEntry == 2020:
            print(double['product'] * nEntry)
    for entry in entries:
        doubles.append({'sum': entry + nEntry, 'product': entry * nEntry})
    entries.append(nEntry)

print("Tough luck")
print(entries)


