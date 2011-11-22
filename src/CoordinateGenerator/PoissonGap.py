'''
@author: matt

required parameters:
    number of points to generate
    per dimension:
        range (low and high)
        
algorithm:
    generate a sequence of 1-dimensional points spaced according to the Poisson Gap algorithm
    (see Hyberts et al, JACS 2010)
    
limitations:
    only works for 1-dimensional points
'''
import math,random
import logging

myLogger = logging.getLogger("poissonGap")

MAX_TRIES = 100


def getGenerator(low, high, numGeneratedPoints):
    def func():
        points = gapMain(numGeneratedPoints, high - low, low)
        return points
    return func


def poisson(lam):
    someNumberL = math.exp(-lam)
    k = 1
    p = random.random()
    while p >= someNumberL:
        p = p * random.random()
        k = k + 1
    return k - 1

def gapMain(numGeneratedPoints, rangeMax, shift):
    adjustmentFactor = 2 * ((rangeMax * 1. / numGeneratedPoints) - 1)
    points = []
    denominator = (rangeMax + 1) * 2
    attempt = 1
    while True:
        i = 0
        while i < rangeMax:
            points.append(i)
            i = i + 1
            lam = adjustmentFactor * math.sin((i + .5) * math.pi / denominator)
            k = poisson(lam)
            i = i + k
        if attempt == MAX_TRIES:
            myLogger.warning("poisson gap didn't converge after " + str(MAX_TRIES) + " iterations -- giving up with best effort")
            break
        elif len(points) == numGeneratedPoints:
            break
        elif len(points) > numGeneratedPoints:
            adjustmentFactor = adjustmentFactor * 1.02
        else:
            adjustmentFactor = adjustmentFactor / 1.02
        points = []
        attempt = attempt + 1
    return map(lambda x: [x + shift], points)
