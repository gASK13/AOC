import common

test_data = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]


def fuel_cost(data):
    costs = []
    for i in range(min(data), max(data)):
        costs.append(sum([abs(x - i) for x in data]))
    return min(costs)


def prepare_costs(max):
    costs = []
    cost = 0
    for i in range(0, max + 1):
        cost += i
        costs.append(cost)
    return costs


def fuel_cost_gradual(data):
    costs = []
    steps = prepare_costs(max(data) - min(data))
    for i in range(min(data), max(data)):
        costs.append(sum([steps[abs(x - i)] for x in data]))
    return min(costs)


print("Part one:")
print(fuel_cost(test_data))
print(fuel_cost(common.Loader.load_matrix(delimiter=',', numeric=True)[0]))

print("\nPart two")
print(fuel_cost_gradual(test_data))
print(fuel_cost_gradual(common.Loader.load_matrix(delimiter=',', numeric=True)[0]))