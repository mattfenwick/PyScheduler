'''
@author: matt

required parameters:
    per dimension:
        range (low and high)
        
algorithm:
    generate a table of n-dimensional points containing all grid points within the given ranges

example:

>>> multipleDimensions([[1,2,3], [2,3,4]])
[[1, 2], [1, 3], [1, 4], [2, 2], [2, 3], [2, 4], [3, 2], [3, 3], [3, 4]]

'''
import ListGenerators as lg

def getGenerator(ranges):
    return lambda: lg.multipleDimensions(ranges)