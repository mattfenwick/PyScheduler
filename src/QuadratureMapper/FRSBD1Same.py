'''
Created on Mar 28, 2011

@author: mattf
'''
#class DependentMapper:
#    def __init__(self, quadChooser):
#        self.quadratureChooser = quadChooser
#    def __call__(self, coordinates):
#        cPoints = map(lambda coors: sc.MultiPhasePoint(coors, self.quadratureChooser()), coordinates)
#        return DependentList(cPoints)
import Schedule.Schedule as sc
import Common
import random


def getGenerator(nDimensions):
    if nDimensions != 2:
        raise ValueError("FRSBD1Same only works for 2-dimensional runs")
    quadChooser = QuadratureChooser()
    def closure(coordinates):
        cPoints = [sc.MultiPhasePoint(coors, [[quadChooser.getQuadrature(coors[0]), 'B']]) for coors in coordinates]
        return Common.DependentList(cPoints)
    return closure


class QuadratureChooser:
    possibleQuadratures = ['R', 'I']
    def __init__(self):
        self.quads = {}
    def getQuadrature(self, coordinate):
        try:
            quad = self.quads[str(coordinate)]
            return quad
        except:
            num = random.randint(0, len(self.possibleQuadratures) -1)
            newQuad = self.possibleQuadratures[num]
            self.quads[str(coordinate)] = newQuad
            return newQuad
