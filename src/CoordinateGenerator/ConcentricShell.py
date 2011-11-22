'''
@author: mattf

required parameters:
    per dimension:
        range (low and high)
        
algorithm:
    generate all points whose distance from the origin is close to a multiple
    of an arbitrary number.  The origin is defined as the point whose coordinates
    are the low end of each dimension's range.
'''
import HyperTable as ht
import math



def getGenerator(ranges, shellSpacing, maxDeviation):
    points = ht.getGenerator(ranges)()
    origin = [r[0] for r in ranges]
    shells = [pt for pt in points if myDist(pt, origin, shellSpacing, maxDeviation)]
    return lambda: shells

    
def myDist(pt, origin, width, maxDeviation):
    dist = distance(pt, origin)
    ratio = dist / width
    return abs(ratio - round(ratio)) * width <= maxDeviation


def distance(pt, origin):
    zipped = zip(pt, origin)
    sumSquares = sum([abs(a - b) ** 2 for (a, b) in zipped])
    dist = math.sqrt(sumSquares)
    return dist