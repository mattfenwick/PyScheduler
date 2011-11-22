'''
@author: mattf

required parameters:
    per dimension:
        low end of range
        
algorithm:
    generate point at high end of ranges

Example:
    in a 2d experiment:
    if range1 = [1,2,3,4] and range2 also equals [1,2,3,4],
    then point [4,4] will be generated
'''

def getSelector(rangeLists):
    maxes = [x[1] for x in rangeLists]
    return lambda: [tuple(maxes)]