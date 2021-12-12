import common

class CaveMap:
    def __init__(self, data):
        self.map = {}
        for line in data:
            s, e = line.split('-')
            self.put(s, e)

    def get_or_create(self, key):
        if key not in self.map:
            self.map[key] = []
        return self.map[key]

    def put(self, start, end):
        self.get_or_create(start).append(end)
        self.get_or_create(end).append(start)

    def find_path_count(self, twice=False):
        stack = [('start', ['start'], 0, False)]
        paths = []
        while len(stack) > 0:
            path = stack.pop()
            if path[0] == 'end':
                paths.append(path)
            else:
                for node in self.map[path[0]]:
                    if node not in path[1] or node.isupper():
                        stack.append((node, path[1] + [node], path[2] + 1, path[3]))
                    elif twice and node in path[1] and not path[3] and node not in ['start', 'end']:
                        stack.append((node, path[1] + [node], path[2] + 1, True))
        #print(paths)
        return paths


test_data = {'example1.txt': (10, 36), 'example2.txt': (19, 103), 'example3.txt': (226, 3509)}

for td in test_data:
    print('Paths in {} = {} (expected {})'.format(
        td, len(CaveMap(common.Loader.load_lines(td)).find_path_count()), test_data[td][0]))
    print('Paths with two caves in {} = {} (expected {})'.format(
        td, len(CaveMap(common.Loader.load_lines(td)).find_path_count(twice=True)), test_data[td][1]))

print('Real paths {}'.format(len(CaveMap(common.Loader.load_lines()).find_path_count())))
print('Real paths #2 {}'.format(len(CaveMap(common.Loader.load_lines()).find_path_count(twice=True))))
