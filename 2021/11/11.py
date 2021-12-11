import common


def flash_fish(_matrix, _x, _y):
    next_flash = []
    for x in range(max(0, _x - 1), min(len(_matrix), _x + 2)):
        for y in range(max(0, _y - 1), min(len(_matrix[0]), _y + 2)):
            if _matrix[x][y] is not None:
                _matrix[x][y] += 1
                if _matrix[x][y] > 9:
                    next_flash.append((x, y))
                    _matrix[x][y] = None
    return next_flash


def step_fish(_matrix):
    flash = []
    flash_count = 0
    for x in range(len(_matrix)):
        for y in range(len(_matrix[0])):
            _matrix[x][y] += 1
            if _matrix[x][y] > 9:
                flash.append((x, y))
                _matrix[x][y] = None

    while len(flash) > 0:
        x, y = flash.pop()
        flash += flash_fish(_matrix, x, y)
        flash_count += 1

    for x in range(len(_matrix)):
        for y in range(len(_matrix[0])):
            if _matrix[x][y] is None:
                _matrix[x][y] = 0

    return flash_count


def find_all_flash(_matrix):
    steps = 0
    while True:
        steps += 1
        if step_fish(_matrix) == len(_matrix) * len(_matrix[0]):
            return steps
        if steps % 10000 == 0:
            print(steps)

test_data = common.Loader.load_matrix('test.txt', numeric=True)
print('9 = {}'.format(sum([step_fish(test_data) for i in range(2)])))

test_data = common.Loader.load_matrix('test2.txt', numeric=True)
print('204 = {}'.format(sum([step_fish(test_data) for i in range(10)])))

test_data = common.Loader.load_matrix('test2.txt', numeric=True)
print('1656 = {}'.format(sum([step_fish(test_data) for i in range(100)])))

test_data = common.Loader.load_matrix(numeric=True)
print('Real {}'.format(sum([step_fish(test_data) for i in range(100)])))

test_data = common.Loader.load_matrix('test2.txt', numeric=True)
print('195 = {}'.format(find_all_flash(test_data)))

test_data = common.Loader.load_matrix(numeric=True)
print('Real {}'.format(find_all_flash(test_data)))