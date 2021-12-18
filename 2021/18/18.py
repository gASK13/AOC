import common


class Node:
    def __init__(self):
        self.parent = None

    def magnitude(self):
        raise NotImplementedError

    def is_list(self):
        raise NotImplementedError

    def explode(self):
        raise NotImplementedError

    def split(self):
        raise NotImplementedError

    @staticmethod
    def __from_array(_list, parent=None):
        if isinstance(_list, list):
            return TreeNode(Node.__from_array(_list[0]), Node.__from_array(_list[1]))
        else:
            return ValueNode(_list)

    @staticmethod
    def from_string(line):
        return Node.__from_array(eval(line))


class TreeNode(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def is_list(self):
        return True

    def explode(self):
        if self.left.is_list() or self.right.is_list():
            raise RuntimeError('OH MY, SHOULD NOT HAPPEN!')
        # find left neighbor
        upptr = self
        while upptr.parent is not None and upptr.parent.left == upptr:
            upptr = upptr.parent
        if upptr.parent is not None:
            upptr = upptr.parent.left
            while upptr.is_list():
                upptr = upptr.right
            upptr.value += self.left.value
        # find right neighbor
        upptr = self
        while upptr.parent is not None and upptr.parent.right == upptr:
            upptr = upptr.parent
        if upptr.parent is not None:
            upptr = upptr.parent.right
            while upptr.is_list():
                upptr = upptr.left
            upptr.value += self.right.value
        # replace by 0
        nn = ValueNode(0)
        self.parent.replace_child(self, nn)

    def replace_child(self, old, new):
        if self.left == old:
            self.left = new
            self.left.parent = self
        else:
            self.right = new
            self.right.parent = self

    def magnitude(self):
        return self.left.magnitude() * 3 + self.right.magnitude() * 2

    def __str__(self):
        return f'[{self.left},{self.right}]'


class ValueNode(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def is_list(self):
        return False

    def split(self):
        nn = TreeNode(ValueNode(self.value // 2), ValueNode(self.value // 2 + (self.value % 2)))
        self.parent.replace_child(self, nn)

    def magnitude(self):
        return self.value

    def __str__(self):
        return f'{self.value}'


def add_snailfish_numbers_in_file(file = None):
    lines = common.Loader.load_lines(file)
    n = Node.from_string(lines.pop(0))
    while len(lines) > 0:
        n = __add_snailfish(n, Node.from_string(lines.pop(0)))
    return n


def find_largest(file = None):
    lines = common.Loader.load_lines(file)
    mags = []
    for line in lines:
        for line2 in lines:
            if line != line2:
                mags.append(__add_snailfish(Node.from_string(line), Node.from_string(line2)).magnitude())
    return max(mags)

def __add_snailfish(a, b):
    line = TreeNode(a, b)
    __reduce_snailfish(line)
    return line


def __reduce_snailfish(line):
    while True:
        if __explode(line):
            continue
        if __split(line):
            continue
        break


def __explode(line):
    # depth first search, depth = 4
    buf = [(line.right, 1), (line.left, 1)]
    while len(buf) > 0:
        node, depth = buf.pop()
        if node.is_list():
            if depth == 4:
                node.explode()
                return True
            else:
                buf.append((node.right, depth + 1))
                buf.append((node.left, depth + 1))
    return False


def __split(line):
    # depth first search, depth = 4
    buf = [(line.right, 1), (line.left, 1)]
    while len(buf) > 0:
        node, depth = buf.pop()
        if node.is_list():
            buf.append((node.right, depth + 1))
            buf.append((node.left, depth + 1))
        elif node.value >= 10:
            node.split()
            return True
    return False


# Tests
n = Node.from_string('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]')
__reduce_snailfish(n)
assert str(n) == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'

# More tests
n = add_snailfish_numbers_in_file('test.txt')
assert str(n) == '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'

n = add_snailfish_numbers_in_file('test2.txt')
assert str(n) == '[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]'
assert n.magnitude() == 4140

n = find_largest('test2.txt')
assert n == 3993

print(f'PT #1: {add_snailfish_numbers_in_file().magnitude()}')
print(f'PT #2: {find_largest()}')