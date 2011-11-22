'''
@author: mattf

overview:
    generate n-dimensional points.
    
interface:
    parameters:  none
    return value:  iterable of n-dimensional points, where each point has the same dimensionality.
        Each point is an iterable of numbers, whose length is the number of dimensions.
'''
import Halton as ha
import HyperTable as ht
import PoissonDisk as pd
import PoissonGap as pg
import ConcentricShell as cs
import Spiral as sp
import Radial as ra
import Utilities as u
import logging


def getObject(params):
    myLogger = logging.getLogger("coordinateGenerator")
    myLogger.debug("determing requested type of coordinate generator....")
    myLogger.debug("parameters used: " + str(params))
    type = params['coordinateGenerator'] # find the requested type
    myLogger.debug("coordinate generator type (" + type + ") found, attempting to find constructor")
    (objectGenerator,_) = generators[type] # find the method for making the coordinate generator 
        #(and fail with an exception if the method can't be found)
    myLogger.debug("constructor found, attempting to build coordinate generator")
    myCGenerator = objectGenerator(params) # build the coordinate generator
    myLogger.debug("coordinate generator successfully built")
    return myCGenerator


def getHalton(params):
    rangeLists = map(lambda dim: dim['range'], params['dimensions'])
    ranges = map(lambda r: u.rangeIncludingBounds(r[0], r[1]), rangeLists)
    numGeneratedPoints = params['numGeneratedPoints']
    return ha.getGenerator(ranges, numGeneratedPoints)


def getHyperTable(params):
    rangeLists = map(lambda dim: dim['range'], params['dimensions'])
    ranges = map(lambda r: u.rangeIncludingBounds(r[0], r[1]), rangeLists)
    return ht.getGenerator(ranges)


def getPoissonDisk(params):
    rangeLists = map(lambda dim: dim['range'], params['dimensions'])
    ranges = map(lambda r: u.rangeIncludingBounds(r[0], r[1]), rangeLists)
    return pd.getGenerator(ranges)


def getPoissonGap(params):
    dimensions = params['dimensions']
    if len(dimensions) != 1:
        raise ValueError("poisson gap algorithm only implemented for one dimension")
    dim1 = dimensions[0]
    low,high = dim1['range']
    numGeneratedPoints = params['numGeneratedPoints']
    return pg.getGenerator(low, high, numGeneratedPoints)


def getConcentricShell(params):
    rangeLists = [dim['range'] for dim in params['dimensions']]
    ranges = [u.rangeIncludingBounds(low, high) for (low, high) in rangeLists]
    shellSpacing = params['shellSpacing']
    maximumDeviation = params['maximumDeviation']
    return cs.getGenerator(ranges, shellSpacing, maximumDeviation)


def getSpiral(params):
    dims = params['dimensions']
    rangeLists = [dim['range'] for dim in dims]
    if len(dims) not in (2, 3):
        raise ValueError("spiral algorithm only implemented for two and three dimensions")
    rstep = params['radiusStep']
    mult = params['angleMultiplier']
    off = params['offsetAngle']
    return sp.getGenerator(rangeLists, rstep, mult, off)


def getRadial(params):
    rangeLists = [dim['range'] for dim in params['dimensions']]
    if len(rangeLists) != 2:
        raise ValueError("radial algorithm only implemented for two dimensions")
    ranges = [u.rangeIncludingBounds(low, high) for (low, high) in rangeLists]
    offset = params['offsetAngle']
    gap = params['gapAngle']
    maxDev = params['maximumDeviation']
    return ra.getGenerator(ranges, offset, gap, maxDev)
    



implementingModules = {'halton':            (getHalton,         ha),
                       'hypertable':        (getHyperTable,     ht),
                       'poissondisk':       (getPoissonDisk,    pd),
                       'poissongap':        (getPoissonGap,     pg),
                       'concentricShell':   (getConcentricShell, cs),
                       'spiral':            (getSpiral,         sp),
                       'radial':            (getRadial,         ra)}

def getImplementingModules():
    return [module for (_, module) in implementingModules.values()]


generators = u.WrappedDictionary(errorMessage = "no such coordinate generator",
                                 dictionary = implementingModules,
                                 enumeratedParameter = "coordinateGenerator")

