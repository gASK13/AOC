import common

test_result = {
    79: {'seed': 79, 'soil': 81, 'fertilizer': 81, 'water': 81, 'light': 74, 'temperature': 78, 'humidity': 78,
         'location': 82},
    14: {'seed': 14, 'soil': 14, 'fertilizer': 53, 'water': 49, 'light': 42, 'temperature': 42, 'humidity': 43,
         'location': 43},
    55: {'seed': 55, 'soil': 57, 'fertilizer': 57, 'water': 53, 'light': 46, 'temperature': 82, 'humidity': 82,
         'location': 86},
    13: {'seed': 13, 'soil': 13, 'fertilizer': 52, 'water': 41, 'light': 34, 'temperature': 34, 'humidity': 35,
         'location': 35}}


def convert_value(mapping, source):
    for (start, end), shift in mapping.items():
        if start <= source <= end:
            return source + shift
    return source


def break_ranges(source_map, ranges):
    # source_map ranges are include on both ends
    # ranges in data are inclusive on both ends
    retranges = []
    while len(ranges) > 0:
        start, end = ranges.pop()
        found = False
        for (s_start, s_end), shift in source_map.items():
            # if it overlaps whole, cool
            if s_start <= start and s_end >= end:
                retranges.append((start + shift, end + shift))
                found = True
                break
            elif s_start > start and s_end < end:
                retranges.append((s_start + shift, s_end + shift))
                ranges.append((start, s_start - 1))
                ranges.append((s_end + 1, end))
                found = True
                break
            elif start < s_start <= end <= s_end:
                retranges.append((s_start + shift, end + shift))
                ranges.append((start, s_start - 1))
                found = True
                break
            elif s_start <= start <= s_end < end:
                retranges.append((start + shift, s_end + shift))
                ranges.append((s_end + 1, end))
                found = True
                break
        # add only when none matched
        if not found:
            retranges.append((start, end))
    return retranges


class Almanac:
    def __init__(self, input_lines):
        self.seed_to_soil = {}
        self.soil_to_fertilizer = {}
        self.fertilizer_to_water = {}
        self.water_to_light = {}
        self.light_to_temperature = {}
        self.temperature_to_humidity = {}
        self.humidity_to_location = {}
        current = None
        for line in input_lines:
            if len(line.strip()) == 0:
                continue
            elif line.startswith('seeds:'):
                self.seeds = [int(_) for _ in line[7:].split(' ')]
            elif line == 'seed-to-soil map:':
                current = self.seed_to_soil
            elif line == 'soil-to-fertilizer map:':
                current = self.soil_to_fertilizer
            elif line == 'fertilizer-to-water map:':
                current = self.fertilizer_to_water
            elif line == 'water-to-light map:':
                current = self.water_to_light
            elif line == 'light-to-temperature map:':
                current = self.light_to_temperature
            elif line == 'temperature-to-humidity map:':
                current = self.temperature_to_humidity
            elif line == 'humidity-to-location map:':
                current = self.humidity_to_location
            else:
                dest_start, source_start, length = [int(_) for _ in line.split(' ')]
                current[(source_start, source_start + length - 1)] = dest_start - source_start

    def get_seed_map(self):
        ret_map = {}
        for seed in self.seeds:
            soil = convert_value(self.seed_to_soil, seed)
            fertilizer = convert_value(self.soil_to_fertilizer, soil)
            water = convert_value(self.fertilizer_to_water, fertilizer)
            light = convert_value(self.water_to_light, water)
            temperature = convert_value(self.light_to_temperature, light)
            humidity = convert_value(self.temperature_to_humidity, temperature)
            location = convert_value(self.humidity_to_location, humidity)

            ret_map[seed] = {'seed': seed, 'soil': soil, 'fertilizer': fertilizer, 'water': water, 'light': light,
                         'temperature': temperature, 'humidity': humidity, 'location': location}
        return ret_map

    def get_min_location_extended(self):
        ranges = []
        for i in range(0, len(self.seeds), 2):
            start = self.seeds[i]
            length = self.seeds[i + 1]
            ranges.append((start, start + length - 1))

        # I want to go through each step in list and break ranges and then recursively call next
        soils = break_ranges(self.seed_to_soil, ranges)
        fertilizers = break_ranges(self.soil_to_fertilizer, soils)
        waters = break_ranges(self.fertilizer_to_water, fertilizers)
        lights = break_ranges(self.water_to_light, waters)
        temperatures = break_ranges(self.light_to_temperature, lights)
        humidities = break_ranges(self.temperature_to_humidity, temperatures)
        locations = break_ranges(self.humidity_to_location, humidities)
        return min([start for start, end in locations])


a = Almanac(common.Loader.load_lines('test'))
assert a.get_seed_map() == test_result
assert min([_['location'] for _ in a.get_seed_map().values()]) == 35
assert a.get_min_location_extended() == 46

print(f'Part 1: {min([_["location"] for _ in Almanac(common.Loader.load_lines()).get_seed_map().values()])}')
print(f'Part 2: {Almanac(common.Loader.load_lines()).get_min_location_extended()}')