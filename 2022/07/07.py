import common


class DiskItem:
    def __init__(self, name):
        self.name = name


class Directory(DiskItem):
    def __init__(self, name, parent):
        super().__init__(name)
        self.parent = parent
        self.items = {}

    def add_item(self, item):
        if item.name not in self.items:
            self.items[item.name] = item
            item.parent = self

    def get_directory(self, name):
        if name not in self.items:
            self.items[name] = Directory(name, self)
        return self.items[name]

    def size(self):
        return sum([i.size() for i in self.items.values()])

    def get_sizes(self):
        retval = [self.size()]
        for i in self.items.values():
            if isinstance(i, Directory):
                retval += i.get_sizes()
        return retval


class File(DiskItem):
    def __init__(self, name, size):
        super().__init__(name)
        self._size = size

    def size(self):
        return self._size


class SystemParser:
    def __init__(self, lines):
        self._root = Directory('/', None)
        self._cwd = self._root
        while len(lines) > 0:
            line = lines.pop(0)
            if line.startswith('$ cd'):
                match line.split(' ')[2]:
                    case '/':
                        self._cwd = self._root
                    case '..':
                        self._cwd = self._cwd.parent
                    case _:
                        self._cwd = self._cwd.get_directory(line.split(' ')[2])
            if line.startswith('$ ls'):
                while len(lines) > 0 and not lines[0].startswith('$'):
                    (size, name) = lines.pop(0).split(' ')
                    if size == 'dir':                        self._cwd.add_item(Directory(name, self._cwd))
                    else:
                        self._cwd.add_item(File(name, int(size)))

    def size(self):
        return self._root.size()

    def get_sizes_under_x(self,x):
        return [s for s in self._root.get_sizes() if s <= x]

    def get_free_space(self):
        return 70000000 - self._root.size()

    def claim_space(self):
        diff = 30000000 - self.get_free_space()
        bigger = [s for s in self._root.get_sizes() if s >= diff]
        bigger.sort()
        return bigger[0]



sp = SystemParser(common.Loader.load_lines('test'))
assert sp.size() == 48381165
assert sum(sp.get_sizes_under_x(100000)) == 95437

print(f'Directories under 100kB sum to : {sum(SystemParser(common.Loader.load_lines()).get_sizes_under_x(100000))}')

assert sp.claim_space() == 24933642

print(f'Smallest dir to claim has size: {SystemParser(common.Loader.load_lines()).claim_space()}')