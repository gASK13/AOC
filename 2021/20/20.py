import common


def neighbors(x, y):
    return [(dx, dy) for dx in range(x - 1, x + 2) for dy in range(y - 1, y + 2)]


# DARK is a flag when the whole image is "lit up" (due to blinking -> pixel in dark go light and vice vera)
# see __get_bit method -> there is a protection for "outside of bounds" and also "dark islands" within data
class Image:
    def __init__(self, data):
        self.__encoder = data.pop(0)
        data.pop(0)
        self.__image = {}
        self.__dark = False
        for y in range(len(data)):
            for x in range(len(data[0])):
                if data[y][x] == '#':
                    self.__image[(x, y)] = 1
                else:
                    self.__image[(x, y)] = 0
        self.__cache_bounds()

    def __cache_bounds(self):
        self.__minx = min([x for (x, y) in self.__image])
        self.__maxx = max([x for (x, y) in self.__image])
        self.__miny = min([y for (x, y) in self.__image])
        self.__maxy = max([y for (x, y) in self.__image])

    def __get_bit(self, x, y):
        if (x, y) in self.__image:
            return self.__image[(x, y)]
        if self.__dark:
            if self.__minx > x or self.__maxx < x or self.__miny > y or self.__maxy < y:
                return 1
        return 0

    def step(self, iterations=1):
        for i in range(iterations):
            new_image = {}
            for x, y in [(x, y) for x in range(self.__minx - 1, self.__maxx + 2) for y in range(self.__miny - 1, self.__maxy + 2)]:
                idx = 0
                for dy in range(y - 1, y + 2):
                    for dx in range(x - 1, x + 2):
                        idx = (idx << 1) | self.__get_bit(dx, dy)
                new_image[(x, y)] = 1 if self.__encoder[idx] == '#' else 0
            if self.__encoder[0] == '#':
                if not self.__dark:
                    self.__dark = True
                elif self.__dark and self.__encoder[511] == '.':
                    self.__dark = False
            self.__image = new_image
            self.__cache_bounds()

    def light_count(self):
        if self.__dark:
            raise RuntimeError("INFINITY")
        return len([i for i in self.__image.values() if i == 1])

    def draw(self):
        print(''.join(self.__encoder))
        print('')
        for y in range(min([y for (x, y) in self.__image]), max([y for (x, y) in self.__image]) + 1):
            line_str = ''
            for x in range(min([x for (x, y) in self.__image]), max([x for (x, y) in self.__image]) + 1):
                line_str += '#' if (x, y) in self.__image else '.'
            print(line_str)


image = Image(common.Loader.load_matrix('test.txt'))
image.step(2)
assert image.light_count() == 35
image.step(50 - 2)
assert image.light_count() == 3351

image = Image(common.Loader.load_matrix())
image.step(2)
print(f'REAL #1 = {image.light_count()}')
assert image.light_count() == 5347
image.step(50 - 2)
print(f'REAL #2 = {image.light_count()}')