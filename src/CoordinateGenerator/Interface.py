'''
Created on Mar 10, 2011

@author: mattf
'''

def example():
    """A coordinate generator must return an iterable object (like a list, or a set, or a tuple).  Each item
    of the container must also be iterable, and have the same number of subitems as all the other items.  
    Each subitem must be a number."""
    points1 = [[1,2], (3,4)]
    points2 = set([(2,3), (13, 17)])
    for point in points1:
        (xCoordinate, yCoordinate) = point
        print "x and y: ", xCoordinate, yCoordinate
    myLengths = []
    for point in points2:
        myLengths.append(len(point))
    print "number of subitems: ", myLengths
    return points1

