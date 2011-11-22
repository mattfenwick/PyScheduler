'''
@author: Matt

required parameters:
    per dimension:
        range (low and high)
        
algorithm:
    generate all points within the bounds that have at least one coordinate equal to zero
    
Example:
    if range1 is [0, 1] and range2 is [-1, 0, 1, 2]
    then points [0, -1], [0, 0], [0, 1], [0, 2] and [1, 0] will be returned as 'special',
    and the rest will be returned as 'normal'.
'''
from operator import mul
import ListGenerators as lg



def getSelector(ranges):
    """parameters:  ranges:  a list of ranges, where each range is a list of numbers ordered low to high
        example range:  [1, 2, 3, 4]
        example list of ranges:  [[1,2,3], [2,3,4]]"""
    def func():
        allPoints = lg.multipleDimensions(ranges)
        zeroPoints = filter(lambda x: reduce(mul, x) == 0, allPoints)
        return zeroPoints
    return func
        