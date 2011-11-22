'''
Created on Mar 8, 2011

@author: mattf
'''
import Schedule.Schedule as s

def getSchedule(text):
    text = text.rstrip()
    lines = text.split('\n')
    points = []
    for l in lines:
        nums = l.rstrip().split(' ')
        #print "nums: ", nums
        numericNums = [int(x) for x in nums]
        points.append(s.MultiPhasePoint(numericNums))
    print "number of points: ", len(points)
    return s.SampleSchedule(points)
