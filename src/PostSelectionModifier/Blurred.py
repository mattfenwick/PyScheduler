'''
@author: mattf

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
