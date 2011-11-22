'''
@author: mattf

required parameters:
    number of dimensions
    
algorithm:
    generate one quadrature component for each point -- the one with only reals
'''
import Common


def getGenerator(nDimensions):
    def closure():
        return [['R'] * nDimensions]
    return Common.DependentMapper(closure)