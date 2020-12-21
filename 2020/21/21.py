class Food:
    def __init__(self, _line):
        split = _line.strip().split(' (contains ')
        self.allergens = split[1][:-1].split(', ')
        self.ingredients = split[0].split(' ')

    def __str__(self):
        return '{} ({})'.format(' + '.join(self.ingredients), ' / '.join(self.allergens))

    def restrict_possible(self, _allergen, _possible):
        if _allergen in self.allergens:
            intersection(_possible, self.ingredients)


def read_file(_name):
    return [Food(line) for line in open(_name, 'r').readlines()]


# Intersects in place (LIST 1)
def intersection(_list1, _list2):
    for to_remove in [item for item in _list1 if item not in _list2]:
        _list1.remove(to_remove)


def count_appearances(_ingredients, _foods):
    cnt = 0
    for ingr in _ingredients:
        for food in _foods:
            if ingr in food.ingredients:
                cnt +=1
    return cnt


# MAIN - PART ONE
foods = read_file('21.txt')

ingredients = set([ingr for food in foods for ingr in food.ingredients])
all_possible = list(ingredients)
allergens = [(a, []) for a in set([alle for food in foods for alle in food.allergens])]

for allergen, possible in allergens:
    possible += all_possible
    for food in foods:
        food.restrict_possible(allergen, possible)
    for p in possible:
        ingredients.discard(p)

print('PART ONE = {}'.format(count_appearances(ingredients, foods)))

final_map = []
while len(allergens) > 0:
    allergens.sort(key=lambda l:len(l[1]))
    key, value = allergens.pop(0)
    value = value[0]
    final_map.append((key, value))
    for allergen, possible in allergens:
        if value in possible:
            possible.remove(value)

final_map.sort(key=lambda l:l[0])
print('PART TWO = {}'.format(','.join([value for key, value in final_map])))