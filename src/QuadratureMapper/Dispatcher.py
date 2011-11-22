'''
@author: mattf

overview:
    when collecting data in an NMR experiment, spectrometers also collect quadrature (real, imaginary, etc.).
    It may be desirable to collect quadrature components of points in random/non-standard ways (such as 
    rotating quadrature).
    
interface:
    parameters: an iterable of n-dimensional points, where each point has the same dimensionality.
        Each point is an iterable of numbers, where the len is the number of dimensions.
    return value:  a list of 'quadrature points', where a 'quadrature point' consists of coordinates
        and zero or more quadratures.  A quadrature is currently defined as an iterable of 'R' and 'I'.
        A 'quadrature point' has quadrature/s that have the same number of phases as its dimensionality.
        Example 2d quadrature:  ['R', 'I']
        There can be multiple points with the same quadratures, if the 'quadrature points' can be independently
        selected, but there should never be any equal 'quadrature points'.
        The list supports the methods 'getPoints' and 'getMultiPhasePoints'.
            getPoints returns all points -- it does not group by coordinates
            getMultiPhasePoints returns MultiPhasePoints -- groups by coordinates
'''
import AllPhasesDependent as apd
import AllPhasesIndependent as api
import SingleRandom as s
import JustReals as j
import FirstRandomSecondBoth as f
import FRSBD1Same as frsb
import NoQuadrature as noq
import logging
import Utilities as u


def getObject(params):
    myLogger = logging.getLogger("quadrature mapper")
    myLogger.debug("determing requested type of quadrature mapper....")
    myLogger.debug("parameters used: " + str(params))
    type = params['quadratureMapper']
    myLogger.debug("quadrature mapper type (" + type + ") found, attempting to find constructor")
    (constructor, _) = selectors[type]
    myLogger.debug("constructor found, attempting to build quadrature mapper")
    myMapper = constructor(params)
    myLogger.debug("quadrature mapper successfully built")
    return myMapper


def getAllDependent(params):
    nDimensions = len(params['dimensions'])
    return apd.getGenerator(nDimensions)


def getAllIndependent(params):
    nDimensions = len(params['dimensions'])    
    return api.getGenerator(nDimensions)


def getSingleRandom(params):
    nDimensions = len(params['dimensions'])     
    return s.getGenerator(nDimensions)


def getJustReals(params):
    nDimensions = len(params['dimensions'])    
    return j.getGenerator(nDimensions)


def getFirstRandomSecondBoth(params):
    nDimensions = len(params['dimensions'])
    return f.getGenerator(nDimensions)


def getFRSBD1Same(params):
    nDimensions = len(params['dimensions'])
    return frsb.getGenerator(nDimensions)


def getNone(params):
    return noq.getGenerator()



implementingModules = {'allPhasesDependent':        (getAllDependent,       apd),
                          'allPhasesIndependent':   (getAllIndependent,     api),
                          'singleRandom':           (getSingleRandom,       s),
                          'justReals':              (getJustReals,          j),
                          'firstRandomSecondBoth':  (getFirstRandomSecondBoth, f),
                          'FRSBD1Same':             (getFRSBD1Same,         frsb),
                          'none':                   (getNone,               noq)}

def getImplementingModules():
    return [module for (_, module) in implementingModules.values()]


selectors = u.WrappedDictionary(errorMessage = "no such quadrature mapper",
                                dictionary = implementingModules,
                                enumeratedParameter = "quadratureMapper")

