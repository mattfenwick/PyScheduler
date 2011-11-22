'''
@author: Matt

overview:
    sometimes, it might be desirable to ensure that certain points are selected.  This
    package implements various algorithms for generating points that must be guaranteed
    to be selected.
    
interface:
    parameters:  none
    return value:  iterable of n-dimensional points, where each point has the same dimensionality.
        Each point is an iterable of numbers, whose length is the number of dimensions.
'''
import AllWithZero as a
import SelectNone as s
import AllLowerBounds as ab
import PointBlock as p
import FirstPoint as fp
import LastPoint as lp
import FirstAndLastPoint as flp
import Halton as ha
import Utilities as u
import logging


def getObject(params):
    myLogger = logging.getLogger("specialPointSelector")
    myLogger.debug("determing requested type of special point selector....")
    myLogger.debug("parameters used: " + str(params))
    type = params['forcedSelector']  # get the type
    myLogger.debug("special point selector type (" + type + ") found, attempting to find constructor")
    (constructor, _) = selectors[type] # find the method that builds it
    myLogger.debug("constructor found, attempting to build special point selector")
    specialSelector = constructor(params) # build the selector
    myLogger.debug("special point selector successfully built")
    return specialSelector


def getAllWithZero(params):
    rangeLists = map(lambda dim: dim['range'], params['dimensions'])
    ranges = map(lambda r: u.rangeIncludingBounds(r[0], r[1]), rangeLists)
    return a.getSelector(ranges)


def getNone(params):
    return s.getSelector()


def getAllLowerBounds(params):
    rangeLists = map(lambda dim: dim['range'], params['dimensions'])
    ranges = map(lambda r: u.rangeIncludingBounds(r[0], r[1]), rangeLists)
    return ab.getSelector(ranges)


def getPointBlock(params):
    blockRangeLists = [dim['blockRange'] for dim in params['dimensions']]
    rangeLists = [dim['range'] for dim in params['dimensions']]
    zipped = zip(blockRangeLists, rangeLists)
    for (b, r) in zipped:
        if b[0] < r[0] or b[1] > r[1]:
            raise ValueError("ranges for point block must be within normal ranges (got " + str(b) + ", normal range was " + str(r) + ")")
    blockRanges = [u.rangeIncludingBounds(r[0], r[1]) for r in blockRangeLists]
    return p.getSelector(blockRanges)


def getFirstPoint(params):
    rangeLists = map(lambda dim: dim['range'], params['dimensions'])
    return fp.getSelector(rangeLists)


def getLastPoint(params):
    rangeLists = map(lambda dim: dim['range'], params['dimensions'])
    return lp.getSelector(rangeLists)


def getFirstAndLastPoint(params):
    rangeLists = map(lambda dim: dim['range'], params['dimensions'])
    return flp.getSelector(rangeLists)


def getHalton(params):
    rangeLists = map(lambda dim: dim['range'], params['dimensions'])
    ranges = map(lambda r: u.rangeIncludingBounds(r[0], r[1]), rangeLists)
    numGeneratedPoints = params['specialHaltonPoints']
    return ha.getGenerator(ranges, numGeneratedPoints)
    



implementingModules = {'allWithZero':       (getAllWithZero,        a),
                      'none':               (getNone,               s),
                      'allLowerBounds':     (getAllLowerBounds,     ab),
                      'pointBlock':         (getPointBlock,         p),
                      'firstPoint':         (getFirstPoint,         fp),
                      'lastPoint':          (getLastPoint,          lp),
                      'firstAndLastPoint':  (getFirstAndLastPoint,  flp),
                      'halton':             (getHalton,             ha) }

def getImplementingModules():
    return [module for (_, module) in implementingModules.values()]


selectors = u.WrappedDictionary(errorMessage = "no such special point selector",
                                dictionary = implementingModules,
                                enumeratedParameter = "forcedSelector")

