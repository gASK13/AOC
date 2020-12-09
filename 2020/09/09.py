import numpy as np
nums = np.array([])
sums = []
flat_sums = None
pre = 25
file = '09.txt'

def checkSums(num, sums):
    for subsum in sums:
        if num in subsum:
            return True
    return False


def findContiguousLength(invalid, size):
    nums = []
    sum = 0
    for line in open(file).readlines():
        num = int(line.strip())
        if len(nums) == size:
            sum -= nums.pop(0)
        sum += num
        nums.append(num)
        if invalid == sum:
            nums.sort()
            return (nums[0], nums[-1])
    return None

#PART ONE
print('### PART ONE ###')
invalid = 0
for line in open(file).readlines():
    num = int(line.strip())
    if len(nums) == pre:
        if not checkSums(num, sums):
            print(num)
            invalid = num
            break
        nums = nums[1:]
        sums.pop(0)
    nums = np.append(nums, num)
    sums.append(nums + num)

#PART TWO
print('### PART TWO ###')
for i in range(2, 1000):
    x = findContiguousLength(invalid, i)
    if x is not None:
        print(x)
        print(x[0] + x[1])
        exit()
