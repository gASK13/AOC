import math
import csv

def digit(n, d):
    return math.floor((n % math.pow(10,d) / math.pow(10, d-1)))

def parameter(arr,pos,i):
    if digit(arr[pos], i+2) == 1:
        return arr[pos+i]
    else:            
        return arr[arr[pos+i]]

def op(pos, arr):
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
        arr[arr[pos+1]] = 5 #HARD CODED for NOW!!!
        return pos+2
    elif(arr[pos] % 10 == 4):
        print(arr[arr[pos+1]])
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

def run(row):
    i = 0
    while i<len(row):
        if(row[i] == 99):
            print('HALT!')
            return
        i = op(i,row)
    
roww = []
with open('5.txt', 'r') as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
    for rw in reader:
        roww = rw

#roww=[3,9,7,9,10,9,4,9,99,-1,8]

i = 0
while i < len(roww):
    roww[i] = int(roww[i])
    i += 1

run(roww)    






                                                