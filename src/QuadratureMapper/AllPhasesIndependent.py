'''
@author: Matt

required parameters:
    number of dimensions
    
algorithm:
    generate all possible quadrature components for each point, but return separate 'quadrature points'
    for each quadrature component.  So, 2 ** n * number of points, where n is the number of dimensions 
    of the point, independently selectable 'quadrature points' are generated.
'''
import ListGenerators as lg
import Common


def getGenerator(nDimensions):
    quads = ['R', 'I']
    quadratures = lg.multipleDimensions([quads] * nDimensions)
    def closure():
        return quadratures
    return Common.IndependentMapper(closure)