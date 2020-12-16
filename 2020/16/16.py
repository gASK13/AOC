import copy
lines = open('16.txt', 'r').readlines()

line = lines.pop(0).strip()
rules = {}
fields = []
while len(line) > 0:
    rule_name = line.split(': ')[0]
    fields.append(rule_name)
    for rng in line.split(': ')[1].split(' or '):
        bounds = rng.split('-')
        for i in range(int(bounds[0]), int(bounds[1]) + 1):
            if i not in rules:
                rules[i] = []
            rules[i].append(rule_name)
    line = lines.pop(0).strip()

lines.pop(0) # yout ticket
line = lines.pop(0).strip()
ticket = [int(n) for n in line.split(',')]

lines.pop(0) # new line
lines.pop(0) # other tickets
other_tickets = []
for line in lines:
    other_tickets.append([int(n) for n in line.strip().split(',')])

print(rules)
print(ticket)
print(other_tickets)

# PART ONE
invalid = []
invalid_sum = 0
for tic in other_tickets:
    invalid_tic = False
    for item in tic:
        if item not in rules:
            invalid_tic = True
            invalid_sum += item
    if invalid_tic:
        invalid.append(tic)

print(invalid_sum)

# PART TWO
for i in invalid:
    other_tickets.remove(i)

possible_fields = [copy.deepcopy(fields) for i in range(0, len(ticket))]
for tic in other_tickets:
    for (idx, item) in enumerate(tic):
        rules_set = rules[item]
        new_fields = []
        for field in possible_fields[idx]:
            if field in rules_set:
                new_fields.append(field)
        possible_fields[idx] = new_fields

print(possible_fields)

field_order = [None for i in range(0, len(ticket))]
while True:
    clear_field = None
    for (idx, f) in enumerate(possible_fields):
        if field_order[idx] is None:
            if len(f) == 1:
                field_order[idx] = f[0]
                clear_field = f[0]
                break
    if clear_field is not None:
        for f in possible_fields:
            if clear_field in f:
                f.remove(clear_field)
    else:
        break

print(field_order)
tic_prod = 1
for (idx, field) in enumerate(field_order):
    if field[:9] == 'departure':
        tic_prod *= ticket[idx]
print(tic_prod)





