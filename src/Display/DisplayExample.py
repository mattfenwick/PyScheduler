'''
Created on Mar 17, 2011

@author: mattf
'''
import logging
import Driver as dr
import jsonWrapper as j
import Display.GraphTest as t
import argparse as a
import Utilities


LOG_FILENAME = "myLog.txt"
logging.basicConfig(filename = LOG_FILENAME, level = logging.DEBUG, filemode = 'w')
    
    
def main():
    parser = a.ArgumentParser(description = "Generate sample schedules")
    parser.add_argument('parameterfile', type=str, help='json formatted file')
    parser.add_argument('savelocation', type=str, help='location to save the generated schedule')
    args = parser.parse_args()
    
    myFile = open(args.parameterfile, 'r')
    params = j.load(myFile)
    doSchedule(params, args.savelocation)
            
        
def doSchedule(parameters, savepath, bool = True):
    try:
        params = Utilities.WrappedDictionary("missing parameter", parameters)
        validateAndMassageParameters(params)
        logging.debug(params)
        (stri, sched) = dr.makeSchedule(params)
        if bool:
            t.displayPoints(sched, params['dimensions'][0]['range'][1], 
                    params['dimensions'][1]['range'][1])
        outfile = open(savepath, 'w')
        outfile.write(stri)
        outfile.close()
    except Exception, e:
        logging.error(e)
        raise
    

def validateAndMassageParameters(parameters):
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

    
def number(x): 
    return x + 3
def string(s): 
    return s + "testString"
def List(l): 
    return l + []
def Range(r):
    return r[0] + 3 + r[1]
    
def typeCheck(parameters):
    """Check whether the types of the parameters are correct as defined in THIS file -- meaning that 
    it's possible that the types as specified in this file are out-of-sync with those in the implementing modules.
    Throws an exception and logs the first type error it detects, if any."""
    types = {"coordinateGenerator" :    string,
             "numGeneratedPoints" :     number,
             "formatter" :              string,
             "pointSelector" :          string,
             "quadratureMapper" :       string,
             "numSelectedPoints" :      number,
             "forcedSelector" :         string,
             "seed" :                   number,
             "dimensions" :             List
        }
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
    types = {"range" :                  Range,
             "decayRate" :              number,
             "sweepWidth" :             number,
             "exponent" :               number,
             "probabilityFunction" :    string,
        }
    for d in dimensions:
        for param in d.keys():
            try:
                checker = types[param]
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


if __name__ == "__main__":
    main()