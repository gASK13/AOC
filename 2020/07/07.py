import re

def parseLine(line):
    split = line.strip().split(' contain ')
    bag = split[0].replace(' bags', '')
    content = {}
    if re.match('no other', split[1]) is None:
        for item in split[1].split(', '):
            item = re.sub(' bags?\.?', '', item)
            count = int(re.match('([0-9]+) ', item).groups()[0])
            item = re.sub('[0-9]+ ', '', item)
            content[item] = count
    return {'color': bag, 'content': content, 'count': 1}

# Parse content
bags = []
reverse = {}
for line in open('07.txt', 'r').readlines():
    bag = parseLine(line)
    bags.append(bag)
    for color in bag['content'].keys():
        if color not in reverse:
            reverse[color] = set()
        reverse[color].add(bag['color'])

# Extra part - now get all possible combination counts
counts = {}
while len(bags) > 0:
    removal = []
    for item in bags:
        if len(item['content']) == 0:
            counts[item['color']] = item['count']
            removal.append(item)
            for applyOnItem in bags:
                if item['color'] in applyOnItem['content']:
                    applyOnItem['count'] += item['count'] * applyOnItem['content'][item['color']]
                    del applyOnItem['content'][item['color']]
    for item in removal:
        bags.remove(item)

print(counts)


# Final set arrangement
new = set()
possible = set()
new.add('shiny gold')

while len(new) > 0:
    curr = new.pop()
    possible.add(curr)
    if curr in reverse:
        for x in reverse[curr]:
            if x not in possible:
                if x not in new:
                    new.add(x)

print('--------------------')
possible.remove('shiny gold')
print(possible)
print(len(possible))

print('--------------------')
print(counts['shiny gold'] - 1)