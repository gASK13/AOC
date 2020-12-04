import math
import csv
from itertools import permutations 

def digit(n, d):
    return math.floor((n % math.pow(10,d) / math.pow(10, d-1)))

def parameter(arr,pos,i):
    if digit(arr[pos], i+2) == 1:
        return arr[pos+i]
    else:            
        return arr[arr[pos+i]]

def op(pos, arr, input, output):
    if(arr[pos] % 10 == 1):
        a = parameter(arr,pos,1)
        b = parameter(arr,pos,2)
        arr[arr[pos+3]] = a + b
        return pos+4
    elif(arr[pos] % 10 == 2):
        a = parameter(arr,pos,1)
        b = parameter(arr,pos,2)
        arr[arr[pos+3]] = a * b
        return pos+4
    elif(arr[pos] % 10 == 3):
        arr[arr[pos+1]] = input.pop(0)
        return pos+2
    elif(arr[pos] % 10 == 4):
        output.append(arr[arr[pos+1]])
        return pos+2
    elif(arr[pos] % 10 == 5):
        a = parameter(arr,pos,1)
        b = parameter(arr,pos,2)
        if a != 0:
            return b                
        return pos+3
    elif(arr[pos] % 10 == 6):
        a = parameter(arr,pos,1)
        b = parameter(arr,pos,2)
        if a == 0:
            return b                
        return pos+3
    elif(arr[pos] % 10 == 7):
        a = parameter(arr,pos,1)
        b = parameter(arr,pos,2)
        if a < b:
            arr[arr[pos+3]] = 1
        else:
            arr[arr[pos+3]] = 0                            
        return pos+4
    elif(arr[pos] % 10 == 8):
        a = parameter(arr,pos,1)
        b = parameter(arr,pos,2)
        if a == b:
            arr[arr[pos+3]] = 1
        else:
            arr[arr[pos+3]] = 0                            
        return pos+4

def run(row, pos, input):
    i = pos
    output = []
    while i<len(row):
        if(row[i] == 99):
            return {'halt': True, 'output': output};
        i = op(i,row, input, output)
        if len(output) > 0:
            return {'halt': False, 'output': output, 'pos': i} 
    
def loadRow():
    roww = []
    with open('7.txt', 'r') as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for rw in reader:
            roww = rw
    
    #roww=[3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
    
    i = 0
    while i < len(roww):
        roww[i] = int(roww[i])
        i += 1
    return roww

perm = permutations([9,8,7,6,5])
max = 0
maxp = []
for p in perm:
    output = [0]
    states = [loadRow(), loadRow(), loadRow(), loadRow(), loadRow()]
    pos = [0,0,0,0,0]
    lastE = 0
    i = 0
    first = True
    while True:
        if first: output = [p[i]] + output 
        ret = run(states[i], pos[i], output)        
        output = ret['output']        
        if (ret['halt'] == True):            
            break
        pos[i] = ret['pos'] 
        i += 1
        if i > 4: 
            i = 0
            lastE = output[0]
            first = False
    if lastE > max:
        max = lastE
        maxp = p
    
print(maxp)
print(max)







                                                