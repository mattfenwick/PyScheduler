'''
Created on Mar 15, 2011

@author: mattf
'''
import Common as c
import random
from math import cos, sin, pi, e # variables in scope that a user can use
import logging

myLogger = logging.getLogger("userDefinedFunction")

def getSelector(expressionStrings, numPointsToSelect):
    dimensionFunctions = [builder(myString) for myString in expressionStrings]
    def probability(coordinates):
        funcsAndArgs = zip(dimensionFunctions, coordinates)
        results = map(lambda (func, arg): func(arg), funcsAndArgs)
        result = reduce(lambda x,y: x * y, results, random.random())
        return result
    return c.ProbabilitySelector(probability, numPointsToSelect)

def builder(s):
    def func(i):
        i = float(i)
        try:
            result = eval(s)
        except NameError, e:
            myLogger.error("invalid variable name in user-defined function (" + str(s) + "): " + e.message)
            raise NameError(e.message + ": please use 'i' in expressions")
        except SyntaxError, e:
            myLogger.error("invalid function syntax in user-defined function (" + str(s) + "): " + e.message)
            raise SyntaxError(e.message + " please correct function < " + str(s) + " >")
        return result
    return func
    