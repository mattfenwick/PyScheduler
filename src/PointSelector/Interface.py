'''
Created on Mar 10, 2011

@author: mattf
'''

# key points to consider:
#    what if there are fewer points in the point pool than the caller wishes to have selected?
def example(pointPool, numberOfPointsToSelect):
    """pointPool is a list of points, where a point list supports the method getPoints,
    and each point supports the method getCoordinates.  numberOfPointsToSelect is a 
    non-negative integer.  What happends if the caller asks for more points to be selected
    than are in the point pool?  This issue has not yet been defined.  What happens if the
    caller requests a negative number of points to be selected?  The method should return 
    a new, empty point list.  pointPool should also support the method newInstance(points), 
    to allow for the creation of a new point list containing the selected points."""
    points = pointPool.getPoints()
    for p in points:
        p.getCoordinates()
    return pointPool.newInstance(points)
    