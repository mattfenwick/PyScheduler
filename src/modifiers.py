'''
required parameters:
    blur width -- each point will be moved in each dimension between 0 and this number of grid units
    per dimension:
        range (min and max)
        
algorithm:
    adjust all of the points a small amount in each dimension.
    For each point, for each dimension, a random number is chosen between (+ blur width) and (- blur width),
    which is the adjustment in that dimension for that point.
    example:
        blur width = 2
        (x,y) = [3, 7]
        blurx = random number between -2 and 2, inclusive = -1
        blury = random number between -2 and 2, inclusive = 2
        blurred point = [x + blurx, y + blury]
        blurred point = [3 + (-1), 7 + 2] = [2, 9]
        
notes:
    This process can create multiple points with identical coordinates.  Therefore, all duplicates are removed; 
    however, if the duplicates have different quadratures, any one of them could be the one that is preserved,
    based on Python's built in set() function using the hash value of only the coordinates.
    Also, any points that end up outside the specified ranges will be removed.
    This results in a number of points less than or equal to the initial number of points.
    
'''
import random
import Schedule.Schedule as sc


def getModifier(rangeLists, blurWidth):
    def closure(points):
        newWrappedPoints = [bumpCoordinates(pt.getCoordinates(), pt.getQuadratures(), blurWidth) for pt in points]
        newUniquePointsByCoordinates = set(newWrappedPoints)# make them unique by coordinates
        blurredPoints = [pt.point for pt in newUniquePointsByCoordinates if inRanges(pt, rangeLists)]# remove any outside the ranges
        return blurredPoints
    return closure


def inRanges(wrappedPoint, rangeLists):
    coors = wrappedPoint.point.getCoordinates() # [18, 4]      [(1,20), (1, 10)] -> [(18, (1, 20)), (4, (1, 10))]
    zipped = zip(coors, rangeLists)
    return all([low <= c <= high for (c, (low, high)) in zipped])


def bumpCoordinates(coors, quads, blurWidth):
    newCoords = [bump(c, blurWidth) for c in coors]
    return WrapperPoint(sc.MultiPhasePoint(newCoords, quads))


def bump(c, blurWidth):
    return c + random.randint(-blurWidth, blurWidth)
    

class WrapperPoint:
    def __init__(self, point):
        self.point = point
    def __hash__(self):
        return hash(tuple(self.point.getCoordinates()))
    def __cmp__(self, other):
        return cmp(self.point.getCoordinates(), other.point.getCoordinates())
        

'''
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
    some other points, either in the original list or in the additional list
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

