import common


def redistribute(_data):
    max_index = _data.index(max(_data))
    tot = _data[max_index]
    _data[max_index] = 0
    while tot > 0:
        max_index += 1
        if max_index >= len(_data):
            max_index -= len(_data)
        _data[max_index] += 1
        tot -= 1


def run_cycles(_data, debug=False):
    seen = {common.hash_list(_data): 0}
    step = 0
    while True:
        redistribute(_data)
        if debug:
            print(_data)
        step += 1
        hash = common.hash_list(_data)
        if hash in seen:
            return step, step - seen[hash]
        seen[hash] = step


print("Test data - steps {}, repeat after {}".format(*run_cycles([0, 2, 7, 0], debug=True)))
print("Real data - steps {}, repeat after {}".format(*run_cycles(common.Loader.load_matrix(delimiter='\t', numeric=True)[0])))
