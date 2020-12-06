class Group:
    def __init__(self):
        self.letters = {}
        self.count = 0
    def addLine(self, line):
        self.count += 1
        for char in line:
            if char not in self.letters:
                self.letters[char] = 0
            self.letters[char] = self.letters[char] + 1
    def oldSize(self):
        return len(self.letters.keys())
    def size(self):
        cnt = 0
        for ltr in self.letters.keys():
            if self.letters[ltr] == self.count:
                cnt += 1
        return cnt


groups = []
grp = Group()
groups.append(grp)
for line in open('06.txt', 'r').readlines():
    line = line.strip()
    if len(line) == 0:
        grp = Group()
        groups.append(grp)
    else:
        grp.addLine(line)

total = 0
for grp in groups:
    print("Group [" + str(grp.size()) + "]: " + str(grp.letters.keys()))
    total += grp.size()

print(total)