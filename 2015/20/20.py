import common
from colorama import Fore, Back, Style
import plotly.graph_objects as go


def compute_house(idx):
    _sum = 0
    for i in range(1, idx + 1):
        if idx % i == 0:
            _sum += i*10
    return _sum


def compute_house_second(idx):
    _sum = 0
    for i in range(1, idx + 1):
        if idx % i == 0 and idx / i <= 50:
            _sum += i*11
    return _sum


def graph_divisors(start, count):
    data = [compute_house_second(x) for x in range(start, start + count)]
    # now draw it in plotly
    fig = go.Figure(data=[go.Scatter(x=list(range(start, start + count)), y=[x for x in data])])
    fig.show()


def find_house(presents, start=1, step=1):
    for i in range(start, presents // 10, step):
        if compute_house(i) >= presents:
            return i
    raise Exception('Not found :(')


def find_house_second(presents, start=1, step=1):
    for i in range(start, presents // 10, step):
        if compute_house_second(i) >= presents:
            return i
    raise Exception('Not found :(')

assert find_house(420) == 20

# Used PLOTLY to find "local maxima" manually
# The biggest step is by "2520" (giving quite nice peaks after 10k)
# then by 60 (giving much smaller subpeaks)
# then by 1 of course (in case we get lucky)

roughest = find_house(29000000, 0, 2520)
rough = find_house(29000000, roughest - 2520, 60)
fine = find_house(29000000, rough - 60, 1)
print(f'Part 1: {Back.GREEN}{Fore.BLACK}{fine}')

roughest = find_house_second(29000000, 0, 2520)
rough = find_house_second(29000000, roughest - 2520, 60)
fine = find_house_second(29000000, rough - 60, 1)
print(f'Part 2: {Back.GREEN}{Fore.BLACK}{fine}')
