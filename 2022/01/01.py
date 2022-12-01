import common


def get_elves(lines):
    lines.append('')

    elves = []
    running = 0
    for l in lines:
        if len(l.strip()) == 0:
            elves.append(running)
            running = 0
        else:
            running += int(l)

    elves.sort(reverse=True)
    return elves


assert get_elves(common.Loader.load_lines('test.txt'))[0] == 24000
print(f'Max is {get_elves(common.Loader.load_lines())[0]}')

assert sum(get_elves(common.Loader.load_lines('test.txt'))[0:3]) == 45000
print(f'Max is {sum(get_elves(common.Loader.load_lines())[0:3])}')
