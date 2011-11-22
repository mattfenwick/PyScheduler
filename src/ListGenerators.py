'''
Created on Jan 27, 2011

@author: mattf
'''


def multipleDimensions(ranges):
    """parameters:  ranges:  an iterable of iterables
    return value:  an list of lists, where the length of the outer list is the product of the length of the
    inner input iterables, and the length of the inner lists is the length of the outer input iterable.
    Each inner list is a combination of one element from each inner iterable."""
    if len(ranges) == 0:
        return [[]]
    else:
        return addDimension(multipleDimensions(ranges[:-1]), ranges[-1])


def flatmapSlow(func, seq):#exhibits terrible growth characteristics
    return reduce(lambda x,y: x + y, map(func, seq), [])

def flatmap(func, seq):
    res = map(func, seq)
    newList = [None] * sum(map(lambda x: len(x), res))
    i = 0
    for x in res:
        for y in x:
            newList[i] = y
            i += 1
    return newList

def addDimension(init_range, new_range):
    return flatmap(lambda x: map(lambda y: x + [y], new_range), init_range)




def nestedMapTest(sequence, rangeGenerator):
    new = flatmap(lambda x: map(lambda y: [x, y], rangeGenerator()), sequence)
    old = flatmap(lambda x: map(lambda y: [x, y], rangeGenerator()), sequence)
    if old != new:
        raise ValueError("should be equal, are not")
    return new

def nestedMap(sequence, rangeGenerator):
    return flatmap(lambda x: map(lambda y: [x, y], rangeGenerator()), sequence)
