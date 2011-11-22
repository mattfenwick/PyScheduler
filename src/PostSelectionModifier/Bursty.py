'''
@author: mattf

required parameters:
    per dimension:
        range (min and max)
        
algorithm:
    for each point in the given collection of points, select additional adjacent points.  
    This results in an increase in the total number of points.
    In each dimension, either the two adjacent points or no extra points are selected,
    based on a random 50/50 choice.  Thus, in three dimensions, either 0, 2, 4, or 6 
    additional points may be selected.  The adjacent points will have the same quadratures
    as the point from which they were generated.
    
notes:
    It is possible that the additional, adjacent points will have equivalent coordinates to
    some other points, either in the original list or in the additional list.  Duplicates will
    be removed using Python's set() function, based on coordinates only -- quadratures are ignored.
'''
from operator import concat
import ListGenerators as lg
import math
import Schedule.Schedule as sc
import random



def getModifier(rangeLists):
    def closure(points):
        newWrappedPoints = reduce(concat, [makeNearbyPoints(pt.getCoordinates(), pt.getQuadratures()) for pt in points])
        newUniquePointsByCoordinates = set(newWrappedPoints)# make them unique by coordinates
        blurredPoints = [pt.point for pt in newUniquePointsByCoordinates if inRanges(pt, rangeLists)]# remove any outside the ranges
        return blurredPoints
    return closure


def inRanges(wrappedPoint, rangeLists):
    coors = wrappedPoint.point.getCoordinates() # [18, 4]      [(1,20), (1, 10)] -> [(18, (1, 20)), (4, (1, 10))]
    zipped = zip(coors, rangeLists)
    return all([low <= c <= high for (c, (low, high)) in zipped])


def makeNearbyPoints(myCoors, quads):
    allCloseCoordinates = lg.multipleDimensions([makeRange(c) for c in myCoors])
    closeEnoughCoordinates = [pt for pt in allCloseCoordinates if distance(myCoors, pt) <= 1]
    return [WrapperPoint(sc.MultiPhasePoint(newCoords, quads)) for newCoords in closeEnoughCoordinates]


def makeRange(c):
    if random.randint(0, 1) == 0:
        return [c - 1, c, c + 1]
    else:
        return [c]


def distance(a, b):
    zipped = zip(a,b)
    return math.sqrt(sum([(c - d) ** 2 for (c, d) in zipped]))

    

class WrapperPoint:
    def __init__(self, point):
        self.point = point
    def __hash__(self):
        return hash(tuple(self.point.getCoordinates()))
    def __cmp__(self, other):
        return cmp(self.point.getCoordinates(), other.point.getCoordinates())
