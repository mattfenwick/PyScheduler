'''
@author: mattf

required parameters:
    number of dimensions
    
algorithm:
    generate one randomly selected quadrature per point
'''
import ListGenerators as lg
import Common
import random


def getGenerator(nDimensions):
    quads = ['R', 'I']
    quadratures = lg.multipleDimensions([quads] * nDimensions)
    length = len(quadratures)
    def closure():
        return [quadratures[random.randint(0, length - 1)]]
    return Common.DependentMapper(closure)