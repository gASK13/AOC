import common


def build_add_on_day(days):
    addons = {}
    for i in range(days + 1):
        addons[i] = 1
        delta = i - 9
        while delta > 0:
            addons[i] += addons[delta]
            delta -= 7

    return addons


def after_days_dynamic(_list, days):
    total = len(_list)
    add_on_day = build_add_on_day(days)
    items = [(item, days) for item in _list]
    while len(items) > 0:
        item = items.pop()
        diff = item[0] - item[1]
        delta = item[1] - item[0]
        while diff < 0:
            total += add_on_day[delta]
            delta -= 7
            diff += 7
    return total


def after_days_normal(_list, days):
    total = len(_list)
    items = [(item, days) for item in _list]
    while len(items) > 0:
        item = items.pop()
        diff = item[0] - item[1]
        delta = item[1] - item[0]
        while diff < 0:
            items.append((8, delta - 1))
            delta -= 7
            diff += 7
            total += 1
    return total


test_list = [3, 4, 3, 1, 2]
test_data = {0: 5, 1: 5, 2: 6, 3: 7, 4: 9, 5: 10, 6: 10, 7: 10, 8: 10, 9: 11, 10: 12, 11: 15, 12: 17, 13: 19, 14: 20,
             15: 20, 16: 21, 17: 22, 18: 26, 80: 5934, 256: 26984457539}

print(build_add_on_day(20))

for i in test_data:
    if i <= 80:
        print('Original algorithm:  {} days {} fish (expected {})'.format(i, after_days_normal(test_list, i),
                                                                          test_data[i]))

for i in test_data:
    print('New algorithm: {} days {} fish (expected {})'.format(i, after_days_dynamic(test_list, i), test_data[i]))


print('Final result {}'.format(after_days_normal(common.Loader.load_matrix(delimiter=',', numeric=True)[0], 80)))
print('Final result, part two {}'.format(after_days_dynamic(common.Loader.load_matrix(delimiter=',', numeric=True)[0],
                                                            256)))

#dynamic programming
