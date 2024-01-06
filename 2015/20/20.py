import common
from colorama import Fore, Back, Style
import plotly.graph_objects as go


def compute_house(idx):
    divisors = []
    for i in range(1, idx + 1):
        if idx % i == 0:
            divisors.append(i)
    return divisors


def graph_divisors(start, count):
    data = [compute_house(x) for x in range(start, start + count)]
    # now draw it in plotly
    fig = go.Figure(data=[go.Scatter(x=list(range(start, start + count)), y=[sum(x) for x in data])])
    fig.show()


def find_house(presents, start=1, step=1):
    for i in range(start, presents // 10, step):
        if sum(compute_house(i)) * 10 >= presents:
            return i
    raise Exception('Not found :(')


assert sum(compute_house(1)) * 10 == 10
assert sum(compute_house(2)) * 10 == 30
assert sum(compute_house(3)) * 10 == 40
assert sum(compute_house(4)) * 10 == 70
assert sum(compute_house(5)) * 10 == 60
assert sum(compute_house(6)) * 10 == 120
assert sum(compute_house(10)) * 10 == 180
assert sum(compute_house(20)) * 10 == 420

assert find_house(420) == 20

# Used to find "local maxima" manually
#graph_divisors(10000, 20000)

# The biggest step is by "2520" (giving quite nice peaks after 10k)
# then by 60 (giving much smaller subpeaks)
# then by 1 of course (in case we get lucky)

roughest = find_house(29000000, 0, 2520)
rough = find_house(29000000, roughest - 2520, 60)
fine = find_house(29000000, rough - 60, 1)
print(f'Part 1: {Back.GREEN}{Fore.BLACK}{fine}')