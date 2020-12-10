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

def match(last, mcount):
    srch = last
    for i in range(len(mcount)):
        if srch.value != mcount[i]:
            return False
        srch = srch.prev
    return True

mcount = [7,6,5,0,7,1] 
#mcount = [5,9,4,1,4]
mcount.reverse()
felf = Node(3, None)
self = Node(7, felf)

rcount = 2
last = self

search = True
while search:
    newnum = str(felf.value + self.value)
    for char in newnum:
        rcount += 1
        last = Node(int(char), last)
        if match(last, mcount):
            print(rcount - len(mcount))
            search = False
            break        
    for i in range(felf.value + 1):
        felf = felf.next
    for i in range(self.value + 1):
        self = self.next


