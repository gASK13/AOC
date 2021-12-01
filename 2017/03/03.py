def distance(num):
    cir = 1
    while cir*cir < num:
        cir += 2
    return (cir - 1)//2 + distance_lateral(num, cir)


def distance_lateral(num, cir):
    if cir == 1:
        return 0
    work_num = num - (cir - 2) * (cir - 2)  # get "working number"
    diff = cir * cir - (cir - 2) * (cir - 2)
    diff = diff // 4
    work_num = work_num % diff
    work_num -= diff // 2
    print("Num is {}, rest is {} at size {}".format(num, work_num, cir -2))
    return work_num

print(distance(1))
print(distance(12))
print(distance(23))
print(distance(1024))

# final
print(distance(289326))