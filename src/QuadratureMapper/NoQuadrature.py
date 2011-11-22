'''
@author: mattf

required parameters:
    none
    
algorithm:
    each point has no quadrature
'''
import Common


def getGenerator():
    def closure():
        return None
    return Common.DependentMapper(closure)