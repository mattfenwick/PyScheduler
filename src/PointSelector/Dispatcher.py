'''
@author: mattf

overview:
    select a number of quadrature points from a collection.  Different sampling schemes
    may have effects on the PSF, sensitivity, and noise of an NMR spectrum.
    
interface:
    parameters:  list of 'quadrature points', number of points already selected
    return value:  list of selected 'quadrature points' containing some subset of the input list
'''
import All as a
import Exponential as e
import Randoms as r
import UserDefined as user 
import AdjustedExponential as ae
import logging
import Utilities as u


def getObject(params):
    myLogger = logging.getLogger("normal point selector")
    myLogger.debug("determing requested type of point selector....")
    myLogger.debug("parameters used: " + str(params))
    type = params['pointSelector']
    myLogger.debug("point selector type (" + type + ") found, attempting to find constructor")
    (constructor, _) = selectors[type]
    myLogger.debug("constructor found, attempting to build point selector")
    mySelector = constructor(params)
    myLogger.debug("point selector successfully built")
    return mySelector


def getAll(params):
    return a.getSelector()


def getExponential(params):
    dimPars = map(extractDimension, params['dimensions'])
    parameters = e.Parameters(dimPars)
    return e.getSelector(parameters, params['numSelectedPoints'])

def extractDimension(dimPars):
    sweepWidth = dimPars['sweepWidth']
    decayRate = dimPars['decayRate']
    exponent = dimPars['exponent']
    return e.DimensionParameters(sweepWidth, decayRate, exponent)


def getRandom(params):
    return r.getSelector(params['numSelectedPoints'])


def getUserDefined(params):
    return user.getSelector(params['dimensions'], params['numSelectedPoints'])



def getAdjustedExponential(params):
    dimPars = map(extractDimension, params['dimensions'])
    factor = params['adjustmentFactor']
    for d in dimPars:
        d.decayRate = d.decayRate * 1. / factor
    parameters = e.Parameters(dimPars)
    return ae.getSelector(parameters, params['numSelectedPoints'])
    

implementingModules = {'all':                   (getAll,                    a),
                      'exponential':            (getExponential,            e),
                      'random':                 (getRandom,                 r),
                      'userDefined':           (getUserDefined,            user),
                      'adjustedExponential':    (getAdjustedExponential,    ae),}

def getImplementingModules():
    return [module for (_, module) in implementingModules.values()]

selectors = u.WrappedDictionary(errorMessage = "no such point selector",
                                dictionary = implementingModules,
                                enumeratedParameter = "pointSelector")

