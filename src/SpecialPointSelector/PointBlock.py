'''
@author: mattf

required parameters:
    per dimension:
        range for point block (low and high)
        
algorithm:    
    generate a table of n-dimensional points containing all grid points within the given block ranges
'''
import ListGenerators as lg


def getSelector(blockRanges):
    def func():
        specialPoints = lg.multipleDimensions(blockRanges)
        return specialPoints
    return func



