def convertToSeat(line):
    row = int(line[0:7].replace('B', '1').replace('F', '0'), 2)
    seat = int(line[7:].replace('L', '0').replace('R', '1'), 2)
    return { 'row' : row, 'seat' : seat, 'ID' : row * 8 + seat}

passes = []
passIds = []
#print(convertToSeat('BFFFBBFRRR'))
#print(convertToSeat('FFFBBBFRRR'))
#print(convertToSeat('BBFFBBFRLL'))
for line in open('05.txt', 'r').readlines():
    line = line.strip()
    seat = convertToSeat(line)
    passes.append(seat)
    passIds.append(seat["ID"])

passIds.sort()

print("Max seat ID: " + str(passIds[len(passIds) - 1]))

for i in range(0, len(passIds) - 2):
    if passIds[i] + 1 != passIds[i+1]:
        print("Your ID: " + str(passIds[i] + 1))