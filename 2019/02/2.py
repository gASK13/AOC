import math
import csv

def op(pos, arr):
    if(arr[pos] == 1):
        arr[arr[pos+3]]=arr[arr[pos+1]] + arr[arr[pos+2]]
    elif(arr[pos] == 2):
        arr[arr[pos+3]]=arr[arr[pos+1]] * arr[arr[pos+2]]

def run(row):
    i = 0
    while i<len(row):
        if(row[i] == 99):
            return row
        op(i,row)
        i += 4
    
def run_prog(a,b):
    roww = []
    with open('2.txt', 'r') as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for rw in reader:
            roww = rw
    
    i = 0
    while i < len(roww):
        roww[i] = int(roww[i])
        i += 1
    
    roww[1] = a
    roww[2] = b
    
    run(roww)    
    #print(roww[0])
    return roww[0]

x = 0
while x<100:
    y = 0
    while y<100:
        z = run_prog(x,y)
        if (z == 19690720):
            print(x)
            print(y)
            print(100*x+y)            
        y+=1
    x+=1





                                                