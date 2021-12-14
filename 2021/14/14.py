import common


def parse_formula(formula):
    formula_dict = {}
    for double in [formula[i:i + 2] for i in range(len(formula) - 1)]:
        if double not in formula_dict:
            formula_dict[double] = 0
        formula_dict[double] += 1
    return formula_dict


def run_on_file(file=None, iterations=10):
    lines = common.Loader.load_lines(file)
    formula = parse_formula(lines[0])
    recipes = {key[0:2]: [key[0] + key[6], key[6] + key[1]] for key in lines[2:]}

    for i in range(iterations):
        new_formula = {}
        for pair in formula:
            for chain in recipes[pair]:
                if chain not in new_formula:
                    new_formula[chain] = 0
                new_formula[chain] += formula[pair]
        formula = new_formula

    # final count of characters - first / last are -1!
    counter = {}
    for pair in formula:
        for c in pair:
            if c not in counter:
                counter[c] = 0
            counter[c] += formula[pair]

    # don't double count all chars - take care of first / last char!
    counter[lines[0][0]] += 1
    counter[lines[0][-1]] += 1
    for c in counter:
        counter[c] //= 2

    return max(counter.values()) - min(counter.values())


print(f'Test = {run_on_file("test.txt")} (expected 1588)')
print(f'Real = {run_on_file()}')

print(f'Test 40 = {run_on_file("test.txt", 40)} (expected 2188189693529)')
print(f'Real 40 = {run_on_file(iterations=40)}')
