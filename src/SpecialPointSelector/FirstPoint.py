'''
@author: mattf

required parameters:
    per dimension:
        low end of range
        
algorithm:
    generate point at low end of ranges

Example:
    in a 2d experiment:
    if range1 = [1,2,3,4] and range2 also equals [1,2,3,4],
    then point [1,1] will be generated
'''

def getSelector(rangeLists):
    mins = [x[0] for x in rangeLists]
    return lambda: [tuple(mins)]
