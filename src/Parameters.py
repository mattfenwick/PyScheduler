'''
@author: mattf

Purpose: specify the types (string, number, etc.) of the parameters and dimension-parameters
that are used by the algorithms, to allow for early type-checking and useful error messages
in case the user input is incorrect.

'''
import Utilities
import logging


    
def number(x): 
    return x + 3
def string(s): 
    return s + "testString"
def List(l): 
    return l + []
def Range(r):
    return r[0] + 3 + r[1]
def Boolean(b):
    if b is True or b is False:
        pass
    else:
        raise TypeError


types = {"coordinateGenerator" :    string,
         "numGeneratedPoints" :     number,
         "formatter" :              string,
         "pointSelector" :          string,
         "quadratureMapper" :       string,
         "numSelectedPoints" :      number,
         "forcedSelector" :         string,
         "postSelectionModifier":   string,
         "shellSpacing":            number,
         "maximumDeviation":        number,
         "radiusStep":              number,
         "angleMultiplier":         number,
         "offsetAngle":             number,
         "gapAngle":                number,
         "seed" :                   number,
         "blurWidth":               number,
         "specialHaltonPoints":     number,
         "dimensions" :             List,
         "formatQuadrature":        Boolean
         }


dimensionTypes = {"range" :                 Range,
                 "decayRate" :              number,
                 "sweepWidth" :             number,
                 "exponent" :               number,
                 "probabilityFunction" :    string,
                 "blockRange" :             Range,
                 }
    
    
def validateAndMassageParameters(parameters):
    """Validate the types of the parameters, and place the dimension parameters in 
    wrapped dictionaries for improved error reporting in the case of a missing dimension parameter."""
    typeCheck(parameters)
    dims = []
    i = 1
    for d in parameters['dimensions']:
        dims.append(Utilities.WrappedDictionary(errorMessage = "missing parameter from dimension " + str(i), 
                                                dictionary = d))
        i += 1
    parameters['dimensions'] = dims
    # are the dimension lows lower than the highs?
    # are things that should be numeric actually numeric?
    # are the numbers all positive?
    # what else can I check for?
    
    
def typeCheck(parameters):
    """Check whether the types of the parameters are correct as defined in THIS file -- meaning that 
    it's possible that the types as specified in this file are out-of-sync with those in the implementing modules.
    Throws an exception and logs the first type error it detects, if any."""
    for param in parameters.getKeys():
        try:
            checker = types[param]
        except KeyError:
            logging.warning("unused parameter: " + param)
            continue
        value = parameters[param]
        try:
            checker(value)
        except TypeError:
            message = "bad type for parameter <" + str(param) + ">:  expected " + checker.func_name + ", got " + str(type(value))
            logging.error(message)
            raise TypeError(message)
    dimensionTypeCheck(parameters['dimensions'])


def dimensionTypeCheck(dimensions):
    # example: list of {"range": [1, 128], "decayRate": 50, "sweepWidth": 16000, "exponent" : 1, "probabilityFunction" : "1 / i"} 
    for d in dimensions:
        for param in d.keys():
            try:
                checker = dimensionTypes[param]
            except KeyError:
                logging.warning("unused parameter: " + param)
                continue
            value = d[param]
            try:
                checker(value)
            except TypeError:
                message = "bad type for dimension parameter <" + str(param) + ">:  expected " + checker.func_name + ", got " + str(type(value))
                logging.error(message)
                raise TypeError(message)
