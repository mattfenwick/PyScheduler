'''
@author: mattf

required parameters:
    number of points to select
    
algorithm:
    randomly select 'quadrature points'
'''
import Common
import random

def getSelector(numPointsToSelect):
    return Common.ProbabilitySelector(randomProbabilityGenerator(), numPointsToSelect)


def randomProbabilityGenerator():
    return lambda x: random.random()