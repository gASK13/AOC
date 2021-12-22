import common


class Cube:
    def __init__(self, line):
        self.on = 1 if line.split(' ')[0] == 'on' else 0

        self.__minx = int(line.split(',')[0].split('=')[1].split('..')[0])
        self.__maxx = int(line.split(',')[0].split('=')[1].split('..')[1])

        self.__miny = int(line.split(',')[1].split('=')[1].split('..')[0])
        self.__maxy = int(line.split(',')[1].split('=')[1].split('..')[1])

        self.__minz = int(line.split(',')[2].split('=')[1].split('..')[0])
        self.__maxz = int(line.split(',')[2].split('=')[1].split('..')[1])

    def __intersects(self, other):
        if (other.__minx <= self.__minx <= other.__maxx
            or other.__minx <= self.__maxx <= other.__maxx) and \
            (other.__miny <= self.__miny <= other.__maxy
             or other.__miny <= self.__maxy <= other.__maxy) and \
            (other.__minz <= self.__minz <= other.__maxz
             or other.__minz <= self.__maxz <= other.__maxz):
            return True
        return False

    def intersects(self, other):
        return self.__intersects(other) or other.__intersects(self)

    def within_bounds(self, nr):
        return nr >= self.__minx >= -nr


cubes = common.Loader.transform_lines(Cube, 'test.txt')
cubes = [c for c in cubes if c.within_bounds(50)]
on_cubes =

for c in cubes:
    for c2 in cubes:
        if c.intersects(c2):
            print("#INTERSECT!")