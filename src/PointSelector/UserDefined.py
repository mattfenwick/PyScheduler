'''
@author: mattf

required parameters:
    number of points to select
    per dimension:
        sweep width
        decay rate
        maximum index
        
algorithm:
    allow the user to specify a probability function for each dimension.  Then, the functions are used to compute
    a probability for each point, and those with the highest probabilities are selected.
    The function is generated from an expression provided by the user
        available variables:
            sw (sweep width)
            dr (decay rate)
            mi (maximum index)
            i (coordinate of the point in that dimension)
            random() (generate a random float between 0 and 1)
            python's math library, including:
                cos
                sin
                pi
                e
                (all other names imported by 'from math import *' in the underlying python interpreter,
                    check your python documentation for a complete list)
            
example expressions:
    1
    cos(i)
    1 / (mi + 1 - i)
    sw * mi / (dr * i)
    
notes:
    make sure that no division-by-zero errors can occur -- these will crash the program
    make sure that there are no other variables used in the expressions besides the ones described above
'''
import Common as c
from random import random
from math import * # variables in scope that a user can use
import logging

myLogger = logging.getLogger("userDefinedVariables")

def getSelector(dimPars, numPointsToSelect):
    dimensionFunctions = [builder(dim) for dim in dimPars] # build a probability function for each dimension
    def probability(coordinates):
        funcsAndArgs = zip(dimensionFunctions, coordinates) # the functions and arguments for each dimension
        results = map(lambda (func, arg): func(arg), funcsAndArgs) # apply the functions to their corresponding arguments
        result = reduce(lambda x,y: x * y, results, random()) # combine probabilities by multiplication, also combine a random number
        return result
    return c.ProbabilitySelector(probability, numPointsToSelect)

def builder(pars):
    """Build a function of type: f(i) = p  where i is the index (increment), and p is the calculated probability.
    Parameter `pars` is a dictionary containing parameters."""
    dim = {} # use this dictionary to provide parameters to build the function
    s = pars['probabilityFunction']
    for x in ['decayRate', 'sweepWidth']: # if either of these is not present, set it to 1
        try:
            dim[x] = pars[x]
        except:
            dim[x] = 1
    try:
        dim['maxIndex'] = pars['range'][1]
    except:
        dim['maxIndex'] = 1
    def func(i, sw = dim['sweepWidth'], dr = dim['decayRate'], mi = dim['maxIndex']):
        i = float(i) # don't want to do integer math
        try:
            result = eval(s) # evaluate the user-supplied expression with variables in scope
            # if there's an exception, catch the exception to add a useful error message, but then rethrow it
        except NameError, e: # trying to use a non-existent variable
            myLogger.error("invalid variable name in user-defined function (" + str(s) + "): " + e.message)
            raise NameError(e.message + ": please use 'i', 'mi', 'dr', and 'sw' in expressions")
        except SyntaxError, e: # user entered an expression whose syntax is not legal python
            myLogger.error("invalid function syntax in user-defined function (" + str(s) + "): " + e.message)
            raise SyntaxError(e.message + " please check function syntax in function <" + str(s) + ">")
        return result
    return func
