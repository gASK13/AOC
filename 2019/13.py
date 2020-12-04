import math
import csv
from itertools import permutations 

scr = {}

def getInput():
    blX = 0
    pdX = 0
    for x in scr.values():
        if x['object'] == 4:
            blX = x['x']
        if x['object'] == 3:
            pdX = x['x']
    if blX < pdX:
        return -1
    elif blX > pdX:
        return 1        
    return 0

def digit(n, d):
    return math.floor((n % math.pow(10,d) / math.pow(10, d-1)))

def parameter(arr,pos,i,base):
    if digit(arr[pos], i+2) == 1:
        return arr[pos+i]
    elif digit(arr[pos], i+2) == 2:
        return arr[arr[pos+i] + base]
    else:            
        return arr[arr[pos+i]]

def setVal(arr,pos,i,base,val):
    if digit(arr[pos], i+2) == 2:
        arr[arr[pos+i] + base] = val
    else:
        arr[arr[pos+i]] = val

def op(pos, arr, output, base):
    if(arr[pos] % 10 == 1):
        a = parameter(arr,pos,1,base[0])
        b = parameter(arr,pos,2,base[0])
        setVal(arr,pos,3,base[0], a + b)
        return pos+4
    elif(arr[pos] % 10 == 2):
        a = parameter(arr,pos,1,base[0])
        b = parameter(arr,pos,2,base[0])
        setVal(arr,pos,3,base[0], a * b)
        return pos+4
    elif(arr[pos] % 10 == 3):
        setVal(arr,pos,1,base[0],getInput())
        return pos+2
    elif(arr[pos] % 10 == 4):
        a = parameter(arr,pos,1,base[0])
        output.append(a)
        return pos+2
    elif(arr[pos] % 10 == 5):
        a = parameter(arr,pos,1,base[0])
        b = parameter(arr,pos,2,base[0])
        if a != 0:
            return b                
        return pos+3
    elif(arr[pos] % 10 == 6):
        a = parameter(arr,pos,1,base[0])
        b = parameter(arr,pos,2,base[0])
        if a == 0:
            return b                
        return pos+3
    elif(arr[pos] % 10 == 7):
        a = parameter(arr,pos,1,base[0])
        b = parameter(arr,pos,2,base[0])
        if a < b:
            setVal(arr,pos,3,base[0], 1)
        else:
            setVal(arr,pos,3,base[0], 0)                   
        return pos+4
    elif(arr[pos] % 10 == 8):
        a = parameter(arr,pos,1,base[0])
        b = parameter(arr,pos,2,base[0])
        if a == b:
            setVal(arr,pos,3,base[0], 1)
        else:
            setVal(arr,pos,3,base[0], 0)                   
        return pos+4
    elif(arr[pos] % 10 == 9):
        a = parameter(arr,pos,1,base[0])
        base[0] += a
        return pos+2

def run(row, pos, input, base):
    i = pos
    output = []
    while i<len(row):
        if(row[i] == 99):
            return {'halt': True, 'output': output};
        i = op(i,row, output, base)
        if len(output) == 3:
            scr[str(output[0]) + "#" + str(output[1])] = {'object': output[2], 'x':output[0], 'y':output[1] }
            output = []
            
    
def loadRow():
    roww = []
    with open('13.txt', 'r') as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for rw in reader:
            roww = rw
    
    #roww=[109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    #roww=[1102,34915192,34915192,7,4,7,99,0]
    #roww=[104,1125899906842624,99]
    
    i = 0
    while i < len(roww):
        roww[i] = int(roww[i])
        i += 1
    for i in range(0,10000):
        roww.append(0);
    roww[0] = 2
    return roww
                             
run(loadRow(), 0, [], [0])['output']        

print(scr['-1#0'])






                                                