'''
@author: mattf

required parameters:
    number of dimensions
    
algorithm:
    generate all possible quadrature components for each point -- 2 ** n quadrature components, where
    n is the number of dimensions of the point
'''
import ListGenerators as lg
import Common


def getGenerator(nDimensions):
    quads = ['R', 'I']
    quadratures = lg.multipleDimensions([quads] * nDimensions)
    def closure():
        return quadratures
    return Common.DependentMapper(closure)