'''
@author: mattf

required parameters:
    per dimension:
        low end of range
        
algorithm:
    generate points at low end and high end of ranges

Example:
    in a 2d experiment:
    if range1 = [1,2,3,4] and range2 also equals [1,2,3,4],
    then points [1,1] and [4,4] will be generated
'''
import FirstPoint as fp
import LastPoint as lp

def getSelector(rangeLists):
    mins = fp.getSelector(rangeLists)()
    maxes = lp.getSelector(rangeLists)()
    points = set(mins + maxes)
    return lambda: points
