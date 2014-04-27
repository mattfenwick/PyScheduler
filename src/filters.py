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
from math import sin, cos, e, pi
import random


#####################################################################
# probability distributions

def exponential_decay(oversampling, dim_pars):
    fs = []
    for pars in dim_pars:
        f_e = partial(eTerm, pars['decay'], pars['sw'], pars['exponent'], oversampling)
        f_j = lambda x: 1                 if 
              (pars['jcoupling'] is None) else 
              partial(jTerm, pars['jcoupling'][0], pars['jcoupling'][1], oversampling)
        f = lambda x: f_e(x) * f_j(x)
        fs.append(f)
    def probability(coordinates):
        results = [f(x) for (f, x) in zip(fs, coordinates)]
        result = reduce(lambda x,y: x * y, results, random.random())
#        print 'for ',coordinates,' got ',result
        return result
    return probability
        
def eTerm(decay_rate, sweep_width, exponent, oversampling, index):
    top = index * decay_rate * 1.
    bottom = sweep_width * oversampling
    result = e ** (-1 * (top / bottom) ** exponent)
    return result
             
def jTerm(type_, freq, oversampling, x):
    if type_ == 'sin':
        return sin(pi * freq * x / oversampling)
    elif type_ == 'cos':
        return cos(pi * freq * x / oversampling)
    raise ValueError("jcoupling: " + type_)


##############################################################
# and now the functions that use the probability distributions

def select_without_replacement():
    """
    (b -> Prob) -> (a -> b) -> Int -> [a] -> [a]
    
    error condition: input too small to fulfil number requested
    """
    pass
    
def select_with_replacement():
    """
    ??? same as above ???
    """
    pass

# maybe this does something useful:
"""
def selectPointsByProbability(points, ampFunc, number):
    probPoints = map(lambda x: [ampFunc(x.getCoordinates()), x], points)
    sortedPoints = sorted(probPoints, key = lambda x: x[0])
    sortedPoints.reverse()
    selected = sortedPoints[:number]
    return map(lambda x: x[1], selected)
"""

