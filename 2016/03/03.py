import common


test_data = {
    '10 110 310': False,
    '10   110    310   ': False,
    '10 110 110': True,
    '110 100 15': True
}


class Triangle:
    def __init__(self, line):
        self._sides = [int(s) for s in line.split()]
        self._sides.sort()

    def isTriangle(self):
        return self._sides[2] < self._sides[0] + self._sides[1]


for td in test_data:
    assert Triangle(td).isTriangle() == test_data[td]

print(f"Valid triangle count: {sum([1 if t.isTriangle() else 0 for t in common.Loader.transform_lines(Triangle)])}")

data = common.loader.Loader.load_matrix(delimiter='\s+', numeric=True)
data = [[str(data[j*3][i]) + ' ' + str(data[j*3 + 1][i]) + ' ' + str(data[j*3 + 2][i]) for j in range(len(data) // 3)] for i in range(len(data[0]))]
count = 0
for line in data:
    for item in line:
        count = count + (1 if Triangle(item).isTriangle() else 0)

print(f"Valid triangle transposed count: {count}")



