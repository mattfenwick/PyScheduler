'''
Created on Mar 10, 2011

@author: mattf
'''

import Common as c


def example(points):
    """points is an iterable object;  each item in points is a point, where each point is a list/tuple of 
    numbers.  Each point must have the same number of coordinates, i.e. each point must have the same
    dimensionality as all the others.  The return value is a list of quadrature points, where the list of
    points supports the methods getPoints, getMultiPhasePoints, and newInstance, and each quadrature point
    supports the method getCoordinates and has a method for returning its quadrature(s).
    What about the quadrature?  Currently this is a bit of a problem:  the implementation just uses the
    string constants 'R' and 'I' for real and imaginary, respectively, but there's no central location
    from which to grab these constants, they're just a bunch of literals scattered throughout the program.
    Each point should have one or more quadrature settings, where each quadrature setting consists of one 
    real/imaginary component for each dimension."""
    myLengths = []
    for point in points:
        print "point: ", point
        myLengths.append(len(point))
    print "lengths (point dimensionalities): ", myLengths
    
    qPoints = [c.SinglePhasePoint((3,4), ['I', 'R']), c.SinglePhasePoint((1,2), ['R', 'I'])]
    returnList = c.DependentList(qPoints)
    print returnList.getMultiPhasePoints()
    print returnList.getPoints()
    return returnList
