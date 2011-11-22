'''
@author: mattf

required parameters:
    number of points to select
    per dimension:
        decay rate
        sweep width
        exponent
        
algorithm:
    select 'quadrature points' based on the following function:
        e ^ (-i * (dr / sw) ^ exp)
    this function is built for each dimension, then all are composed, to give the probability
'''
import math as m
import random
import Common


def getSelector(params, numPointsToSelect):
    return Common.ProbabilitySelector(originalProbabilityGenerator(params), numPointsToSelect)


def originalProbabilityGenerator(parameters):
    eFuncs = map(lambda dimPars: eTerm(dimPars, parameters.oversampling), parameters.dimensions)
    jFuncs = map(lambda dimPars: jTerm(dimPars, parameters.oversampling), parameters.dimensions)
    def probability(coordinates):
        funcsAndArgs = zip(eFuncs, jFuncs, coordinates)
        results = map(lambda x: x[0](x[2]) * x[1](x[2]), funcsAndArgs)
        result = reduce(lambda x,y: x * y, results, random.random())
#        print 'for ',coordinates,' got ',result
        return result
    return probability
        
def eTerm(pars, oversampling):
    def func(index):
        top = index * pars.decayRate * 1.
        bottom = pars.sweepWidth * oversampling
        result = m.e ** (-1 * (top / bottom) ** pars.exponent)
        return result
    return func
             
def jTerm(pars, oversampling):
    if pars.jcoupling['type'] == 'sin':
        return lambda x: m.sin(m.pi * pars.jcoupling['freq'] * x / oversampling)
    elif pars.jcoupling['type'] == 'cos':
        return lambda x: m.cos(m.pi * pars.jcoupling['freq'] * x / oversampling)
    elif pars.jcoupling['type'] == 'none':
        return lambda x: 1
    else:
        ValueError("jcoupling: " + pars.jcoupling['type'])
        
class DimensionParameters:
    def __init__(self, sweepWidth = 8000, decayRate = 150, exponent = 1):
        self.sweepWidth = sweepWidth
        self.decayRate = decayRate
        self.exponent = exponent
        self.jcoupling = {'type':'none', 'freq':1}

class Parameters:
    def __init__(self, dimPars):
        self.dimensions = dimPars
        self.oversampling = 1
