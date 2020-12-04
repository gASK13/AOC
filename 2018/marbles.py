class Node:
    def __init__(self, value, after=None):
        self.value = value
        if (after == None):
            self.next = self
            self.prev = self
        else:
            self.next = after.next
            self.prev = after
            after.next = self
            self.next.prev = self     
    def remove(self):
        self.next.prev = self.prev
        self.prev.next = self.next
        return self.next   

pcount = 418
#pcount = 9
mcount = 7133900 
#mcount = 25
cmarble = Node(0, None)
rootMarble = cmarble 
players = [0 for x in range(pcount)]

for i in range(1,mcount+1):
    if (i % 23 == 0):
        players[i % pcount] += i
        for x in range(7):
            cmarble = cmarble.prev
        players[i % pcount] += cmarble.value
        cmarble = cmarble.remove()
    else:
        cmarble = Node(i, cmarble.next) 

max = 0
for i in players:
    if i > max: max = i

print(max)



