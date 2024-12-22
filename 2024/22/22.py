import common
from colorama import Fore,Back,Style

test_data = [123,15887950,16495136,527345,704524,1553684,12683156,11100544,12249484,7753432,5908254]

def evolve_secret(secret):
    secret = prune(mix(secret, secret*64))
    secret = prune(mix(secret, int(secret/32)))
    secret = prune(mix(secret, secret * 2048))
    return secret

def run_evolution(secret, iterations):
    changes = (None,None,None,None)
    prices = {}
    for i in range(iterations):
        new_s = evolve_secret(secret)
        changes = (changes[1], changes[2], changes[3], (new_s % 10 - secret % 10))
        if changes[0] is not None:
            if changes not in prices:
                prices[changes] = new_s % 10
        secret = new_s
    return secret, prices


def mix(secret, value):
    return secret ^ value

def prune(secret):
    return secret % 16777216

def part_one(numbers):
    return sum([run_evolution(num, 2000)[0] for num in numbers])

def part_two(numbers):
    totals = {}
    for num in numbers:
        _, prices = run_evolution(num, 2000)
        for k,v in prices.items():
            if k not in totals:
                totals[k] = 0
            totals[k] += v
    mx = max(totals.values())
    for k,v in totals.items():
        if v == mx:
            print(f'Found {k} with {v}')
    return mx

for i in range(len(test_data)-1):
    assert evolve_secret(test_data[i]) == test_data[i+1]

assert part_one([1,10,100,2024]) == 37327623
print(f'Part one: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines(numeric=True))}{Style.RESET_ALL}')

assert part_two([1,2,3,2024]) == 23
print(f'Part two: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines(numeric=True))}{Style.RESET_ALL}')
