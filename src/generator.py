from math import cos, sin, sqrt, pi, atan2, exp
import itertools
import random



def table(ranges):
    return itertools.product(*[range(low, high) for (low, high) in ranges])


def spiral2D(rangeLists, rstep, a2, offset):
    points = []
    ((xl, xh), (yl, yh)) = rangeLists
    xspan, yspan = xh - xl, yh - yl
    r = 0
    radianOffset = offset * pi / 180
    while r <= sqrt(xspan ** 2 + yspan ** 2):
        theta = a2 * r + radianOffset
        x = abs(int(r * cos(theta))) + xl
        y = abs(int(r * sin(theta))) + yl
        if x <= xh and y <= yh:
            points.append((x, y))
        r = r + rstep
    pointSet = set(points)
    return pointSet


def spiral3D(rangeLists, rstep, a2, b):
    points = []
    ((xl, xh), (yl, yh), (zl, zh)) = rangeLists
    xspan, yspan, zspan = xh - xl, yh - yl, zh - zl
    r = 0
    phiA, phiB = 100, 20
    while r <= sqrt(xspan ** 2 + yspan ** 2 + zspan **2):
        theta = a2 * r + b
        phi = phiA * r + phiB
        x = abs(int(r * sin(theta) * cos(phi))) + xl
        y = abs(int(r * sin(theta) * sin(phi))) + yl
        z = abs(int(r * cos(theta))) + zl
        if x <= xh and y <= yh and z <= zh:
            points.append((x, y, z))
        r = r + rstep
    pointSet = set(points)
    return pointSet



def radial(ranges, offsetAngle, gapAngle, maximumDeviation):
    '''
        generate coordinates of points, where the points lie along 'spokes' radiating out from the origin
    '''
    allPoints = table(ranges)
    origin = [r[0] for r in ranges]
    points = [pt for pt in allPoints if radialFilter(pt, origin, offsetAngle, gapAngle, maximumDeviation)]
    return points
    
    
def radialFilter(pt, origin, offsetAngle, degreeGap, tolerance):
    y,x = pt[0] - origin[0], pt[1] - origin[1]
    theta = atan2(x, y) * 180. / pi # angle in degrees
    ratio = (theta + offsetAngle) / degreeGap
    return abs(ratio - round(ratio)) * degreeGap < tolerance



def poisson_gap(max_tries, low, high, numGeneratedPoints):
    '''
    algorithm:
        generate a sequence of 1-dimensional points spaced according to the Poisson Gap algorithm
        (see Hyberts et al, JACS 2010)
        
    limitations:
        only works for 1-dimensional points
    '''
    points = gapMain(max_tries, numGeneratedPoints, high - low, low)
    return points

def poisson(lam):
    someNumberL = exp(-lam)
    k = 1
    p = random.random()
    while p >= someNumberL:
        p = p * random.random()
        k = k + 1
    return k - 1

def gapMain(MAX_TRIES, numGeneratedPoints, rangeMax, shift):
    adjustmentFactor = 2 * ((rangeMax * 1. / numGeneratedPoints) - 1)
    points = []
    denominator = (rangeMax + 1) * 2
    attempt = 1
    while True:
        i = 0
        while i < rangeMax:
            points.append(i)
            i = i + 1
            lam = adjustmentFactor * sin((i + .5) * pi / denominator)
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



primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

def halton(ranges, numGeneratedPoints):
    scalingFactors = [max(x) - min(x) for x in ranges]
    shifts = [min(x) for x in ranges]
    if len(ranges) > len(primes):
        raise ValueError("sorry, not enough primes defined....please define more or reduce the number of dimensions")
    zippered = zip(scalingFactors, shifts, primes)#[(60, 2), (75, 3)]
    sequences = map(lambda (factor, shift, prime): scaledShiftedSequence(factor, shift, prime, numGeneratedPoints), zippered)
    possiblyRedundantPoints = zip(*sequences)
    myPoints = set(possiblyRedundantPoints)
    if len(myPoints) != numGeneratedPoints:
        logging.getLogger("haltonGenerator").warning("halton generator tried to generate " + str(numGeneratedPoints) + 
                                                     " points but only generated " + str(len(myPoints)))
    return myPoints
            
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



def concentric_shell(ranges, shellSpacing, maxDeviation):
    '''
    algorithm:
        generate all points whose distance from the origin is close to a multiple
        of an arbitrary number.  The origin is defined as the point whose coordinates
        are the low end of each dimension's range.
    '''
    points = table(ranges)
    origin = [r[0] for r in ranges]
    shells = [pt for pt in points if myDist(pt, origin, shellSpacing, maxDeviation)]
    return lambda: shells
    
def myDist(pt, origin, width, maxDeviation):
    dist = distance(pt, origin)
    ratio = dist / width
    return abs(ratio - round(ratio)) * width <= maxDeviation

def distance(pt, origin):
    zipped = zip(pt, origin)
    sumSquares = sum([abs(a - b) ** 2 for (a, b) in zipped])
    dist = sqrt(sumSquares)
    return dist



def all_lower_bounds(ranges):
    """
    algorithm:
        generate all points which have at least one coordinate equal to one of the lower bounds as defined by the ranges

    Example:
        in a 2d experiment:
        if range1 = [1,2,3,4] and range2 also equals [1,2,3,4],
        then points [1,1], [1,2], [1,3], [1,4], [2,1], [3,1], [4,1] will be generated
    """
    mins = [x[0] for x in ranges]
    allPoints = lg.multipleDimensions(ranges)
    specialPoints = filter(lambda x: not (my_alb_filter(x, mins)), allPoints)
    return specialPoints

def my_alb_filter(point, mins):
    zipped = zip(point, mins)
    return all([d[0] != d[1] for d in zipped])



def first_point(ranges):
    '''
    algorithm:
        generate point at low end of ranges
    '''
    mins = [x[0] for x in rangeLists]
    return [tuple(mins)]



def last_point(ranges):
    '''
    algorithm:
        generate point at high end of ranges
    '''
    maxes = [x[1] for x in rangeLists]
    return [tuple(maxes)]



def first_and_last(ranges):
    '''
    algorithm:
        generate points at low end and high end of ranges
    '''
    mins = first_point(ranges)
    maxes = last_point(ranges)
    points = set(mins + maxes)
    return points

