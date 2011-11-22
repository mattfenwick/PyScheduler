'''
Created on Mar 10, 2011

@author: mattf
'''


def example(points):
    """points is an iterable object;  each item in points is a point, where each point is a list/tuple of 
    numbers.  Each point must have the same number of coordinates, i.e. each point must have the same
    dimensionality as all the others.  
    The return value is a tuple of (poolOfNormalPoints, speciallySelectedPoints), where the first item
    is a tuple/list of the leftover points available for normal selection, and the second item is a tuple/list
    of the specially selected points.
    There should be no overlap between 'normal' and 'special'."""
    normal = points[:3]
    special = points[3:]
    return (normal, special)
