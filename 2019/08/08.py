import re
import operator

line = open('08.txt', 'r').readline()


class Layer:
    def __init__(self, layer):
        self.layer = layer

    def count(self, char):
        return len(re.findall(char, self.layer))

    def __str__(self):
        return self.layer

    def __repr__(self):
        return self.layer


layers = []

width = 25
height = 6
for i in range(0, len(line) - 1, width * height):
    layer = line[i:(i + width * height)]
    layers.append(Layer(layer))

print(len(layers))

# PART ONE
sorted = [] + layers
sorted.sort(key = operator.methodcaller('count', '0'))
print(sorted[0])
print(sorted[0].count('1') * sorted[0].count('2'))

# PART TWO
for i in range(0, height):
    line = ''
    for j in range(0, width):
        for layer in layers:
            if layer.layer[(i*width) + j] != '2':
                line += layer.layer[(i*width) + j]
                break
    print(line.replace("1", "X").replace("0", " "))
