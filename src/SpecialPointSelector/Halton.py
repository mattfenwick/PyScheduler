'''
@author: Matt

required parameters:  
    number of points to generate
    per dimension:
        range (low and high)

algorithm:
    generate subrandom sequence of n-dimensional points according to the Halton sequence
'''
import logging

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def getGenerator(ranges, numGeneratedPoints):
    scalingFactors = [max(x) - min(x) for x in ranges]
    shifts = [min(x) for x in ranges]
    if len(ranges) > len(primes):
        raise ValueError("sorry, not enough primes defined....please define more or reduce the number of dimensions")
    def func():
        zippered = zip(scalingFactors, shifts, primes)#[(60, 2), (75, 3)]
        sequences = map(lambda (factor, shift, prime): scaledShiftedSequence(factor, shift, prime, numGeneratedPoints), zippered)
        possiblyRedundantPoints = zip(*sequences)
        myPoints = set(possiblyRedundantPoints)
        if len(myPoints) != numGeneratedPoints:
            logging.getLogger("haltonGenerator").warning("halton generator tried to generate " + str(numGeneratedPoints) + 
                                                         " points but only generated " + str(len(myPoints)))
        return myPoints
    return func
    
        
def scaledShiftedSequence(factor, shift, prime, numberOfPoints):
    return map(lambda x: int(factor * x) + shift, haltonSequence(prime, numberOfPoints))


def haltonSequence(prime, length):
    return map(lambda x: haltonNumber(x, prime), range(length))


def haltonNumber(index, base):
    result = 0
    f = 1. / base
    i = index
    while i > 0:
        result = result + f * (i % base)
        i = int(i / base)
        f = f / base
    return result