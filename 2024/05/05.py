import common
from colorama import Fore, Back

def cascading_fix(rules, item, seen, items):
    if item in rules:
        for rule in rules[item]:
            if rule in items and rule not in seen:
                # ouch, it might skip other rules (sad)
                cascading_fix(rules, rule, seen, items)
                seen.append(rule)

def check_rules(rules, line, fix=False):
    seen = []
    if len(line) == 0:
        return 0
    items = line.split(',')
    for item in items:
        if item in seen:
            # we skipped it
            continue
        if item in rules and not all([rule in seen for rule in rules[item] if rule in items]):
            if not fix:
                return 0
            cascading_fix(rules, item, seen, items)
        seen.append(item)
    return int(seen[len(seen) // 2])

assert check_rules({'10': ['11']}, '11,10,9') == 10
assert check_rules({'10': ['11', '13']}, '11,10,9') == 10
assert check_rules({'10': ['11']}, '7,8,11,9,10') == 11
assert check_rules({'10': ['11', '7'], '8' : ['7']}, '7,8,11,9,10') == 11
assert check_rules({'10': ['7'], '7' : ['3']}, '10,11,7,3,5') == 0
assert check_rules({'10': ['7'], '7' : ['3']}, '10,11,7,3,5', True) == 10
assert check_rules({'9': ['11']}, '3,9,11') == 0
assert check_rules({'9': ['11']}, '3,9,11', True) == 11

def order_pages(lines, fix=False):
    rules = {}
    while len(lines[0].strip()) > 0:
        line = lines.pop(0).strip()
        key, value = line.split('|')
        if value not in rules:
            rules[value] = []
        rules[value].append(key)

    # now run items
    cnt = 0
    for line in lines:
        if check_rules(rules, line) > 0:
            cnt += check_rules(rules, line) if not fix else 0
        elif fix:
            cnt += check_rules(rules, line,fix)
    return cnt

assert order_pages(common.Loader.load_lines('test')) == 143
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{order_pages(common.Loader.load_lines())}{Fore.RESET}{Back.RESET}')

assert order_pages(common.Loader.load_lines('test'), True) == 123
print(f'Part 2: {Fore.BLACK}{Back.GREEN}{order_pages(common.Loader.load_lines(), True)}{Fore.RESET}{Back.RESET}')

#6739 it too high!!!!

