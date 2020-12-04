class Tree:
    def __init__(self):
        self.children = []
        self.metadata = []
    def metasum(self):
        total = 0
        for meta in self.metadata:
            total += meta
        return total
    def sum(self):
        total = self.metasum()
        for child in self.children:
            total += child.sum()
        return total
    def value(self):
        if (len(self.children) == 0):
            return self.metasum()
        total = 0            
        for meta in self.metadata:
            if (meta <= len(self.children)):
                total += self.children[meta-1].value()
        return total
    def __str__(self):
        return 'CH: ' + str(len(self.children)) + ', ' + str(self.metadata)
    def __repr__(self):
        return 'CH: ' + str(len(self.children)) + ', ' + str(self.metadata)

        

def parseNode(entries):
    result = Tree()
    childCount = int(entries.pop(0))
    metaCount = int(entries.pop(0))
    for i in range(childCount):
        result.children.append(parseNode(entries))
    for i in range(metaCount):
        result.metadata.append(int(entries.pop(0)))
    return result


entries = open('meta.txt', 'r').readlines()[0].rstrip().split(' ')
tree = parseNode(entries)

    