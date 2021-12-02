from common.loader import Loader

num = Loader.load_lines(numeric=True)
inc = 0
windows_size = 3

for i in range(windows_size + 1, len(num) + 1):
    if sum(num[i-windows_size:i]) > sum(num[i - windows_size-1:i-1]):
        #print(str(num[i - windows_size:i]) + " > " + str(num[i - windows_size - 1:i - 1]))
        inc += 1

print(str(inc))


