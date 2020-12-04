from dateutil.parser import parse
from datetime import timedelta  

# parse line into object
def isGuard(line):
    return '#' in line

def parseGuardId(line):
    line = line.rstrip()
    return int(line.split('#')[1].split(' ')[0])

def parseLine(line, grd):
    line = line.rstrip()
    grd['schedule'].append(parse(line.split(']')[0].split('[')[1]))

def getSleepTotal(grd):
    tot = 0
    i = 0
    while i+1<len(grd['schedule']):
        tot += (grd['schedule'][i+1] - grd['schedule'][i]).seconds
        i += 2
    return tot / 60 

def fTime(t):
    return str(t.hour) + '-' + str(t.minute)


def maxSleep(grd):
    i = 0
    sleep = {}
    while i+1<len(grd['schedule']):
        start = grd['schedule'][i]
        end = grd['schedule'][i+1]
        dtx = start
        while dtx < end:
            if (sleep.get(fTime(dtx)) == None): sleep[fTime(dtx)] = 0
            sleep[fTime(dtx)] += 1
            dtx = dtx + timedelta(minutes = 1) 
        i += 2
    
    mx = 0
    mxkey = ''
    for s in sleep:
        if (mx < sleep[s]):
            mx = sleep[s]
            mxkey = s
    
    return { 'maxSleep' : mx, 'maxMinute' : mxkey }

# group by guard
# tally asleep minutes for each one
# find most likely minute for it



fl = open('guard.txt', 'r')
lines = fl.readlines()
lines.sort()
grds = {}
grd = {}
for line in lines:
    if (isGuard(line)):
        id = parseGuardId(line)
        if grds.get(id) != None:
            grd = grds[id]
        else:
            grd = { 'id' : id, 'schedule' : [] }
            grds[id] = grd
    else:
        parseLine(line, grd)

maxgrd = {}
maxtot = { 'maxSleep' : 0, 'maxMinute' : 'N/A' }
for guard in grds.values():
    tot = maxSleep(guard)
    if (tot['maxSleep'] > maxtot['maxSleep']):
        maxgrd = guard
        maxtot = tot

