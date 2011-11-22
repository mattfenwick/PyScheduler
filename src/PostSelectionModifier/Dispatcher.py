'''
@author: mattf

overview:
    after points have been selected, it may be desirable to apply a technique that has a slight effect
    on the distribution, that perhaps shifts points a couple of grid units but does not have a large
    effect on the overall distribution.  This can be important in reducing the noise peaks in the
    point-spread function.
    
interface:
    parameters: an iterable of n-dimensional quadrature points, where each point has the same dimensionality.
        Each point is an iterable of numbers, where the length is the number of dimensions.
    return value:  a set of 'quadrature points', where a 'quadrature point' consists of coordinates
        and zero or more quadratures.  A quadrature is currently defined as an iterable of 'R' and 'I'.
        A 'quadrature point' has quadrature/s that have the same number of phases as its dimensionality.
        Example 2d quadrature:  ['R', 'I']
        The 'setness' of the collection is based on the coordinates of each point -- so there are no two
        points with the same coordinates.
'''
import NoModification as n
import Bursty as br
import Blurred as bl
import logging
import Utilities as u


def getObject(params):
    myLogger = logging.getLogger("post selection modifier")
    myLogger.debug("determing requested type of post selection modifier....")
    myLogger.debug("parameters used: " + str(params))
    type = params['postSelectionModifier']
    myLogger.debug("post selection modifier type (" + type + ") found, attempting to find constructor")
    (constructor, _) = modifiers[type]
    myLogger.debug("constructor found, attempting to build post selection modifier")
    mySelector = constructor(params)
    myLogger.debug("post selection modifier successfully built")
    return mySelector


def getNone(params):
    return n.getModifier()


def getBlurred(params):
    rangeLists = [d['range'] for d in params['dimensions']]
    blurWidth = params['blurWidth']
    return bl.getModifier(rangeLists, blurWidth)


def getBursty(params):
    rangeLists = [d['range'] for d in params['dimensions']]
    return br.getModifier(rangeLists)
    

implementingModules = {'none':                  (getNone,               n),
                      'blurred':                (getBlurred,            bl),
                      'bursty':                 (getBursty,             br),}

def getImplementingModules():
    return [module for (_, module) in implementingModules.values()]

modifiers = u.WrappedDictionary(errorMessage = "no such post-selection modifier",
                                dictionary = implementingModules,
                                enumeratedParameter = "post-selection modifier")

