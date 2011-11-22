'''
@author: mattf

required parameters:
    per dimension:
        range (low and high)
        
algorithm:
    generate all points which have at least one coordinate equal to one of the lower bounds as defined by the ranges

Example:
    in a 2d experiment:
    if range1 = [1,2,3,4] and range2 also equals [1,2,3,4],
    then points [1,1], [1,2], [1,3], [1,4], [2,1], [3,1], [4,1] will be generated
'''

import ListGenerators as lg

def getSelector(ranges):
    """parameters:  ranges:  a list of ranges, where each range is a list of numbers ordered low to high
        example range:  [1, 2, 3, 4]
        example list of ranges:  [[1,2,3], [2,3,4]]"""
    mins = [x[0] for x in ranges]
    def func():
        allPoints = lg.multipleDimensions(ranges)
        specialPoints = filter(lambda x: not (myFilter(x, mins)), allPoints)
        return specialPoints
    return func


def myFilter(point, mins):
    zipped = zip(point, mins)
    return all([d[0] != d[1] for d in zipped])



def test():
    func = getSelector([range(3,5), range(1,3), range(2,4)])
    (a, b) = func(lg.multipleDimensions([range(1,4), range(1,5), range(2,6)]))
    print a
    print b
    