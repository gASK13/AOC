import common


def get_groups(data):
    grouped_data = [set([program for subrule in rule.split(' <-> ') for program in subrule.split(', ')]) for rule in data]
    merged = True
    while merged:
        merged = False
        new_groups = []
        while len(grouped_data) > 0:
            grp = grouped_data.pop()
            for new_grp in new_groups:
                if len(grp & new_grp) > 0:
                    new_grp.update(grp)
                    merged = True
                    grp = None
                    break
            if grp is not None:
                new_groups.append(grp)
        grouped_data = new_groups

    return grouped_data


def find_zero(data):
    for grp in data:
        if '0' in grp:
            print('0 is in group with {} elements (total groups {})'.format(len(grp), len(data)))


test_grps = get_groups(common.Loader.load_lines('test.txt'))
find_zero(test_grps)

grps = get_groups(common.Loader.load_lines())
find_zero(grps)
