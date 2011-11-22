'''
Created on Jan 27, 2011

@author: mattf
'''
import ListGenerators as lg
import Schedule.Schedule as sc


class SinglePhasePoint:

    def __init__(self, coordinates, quadrature):
        if len(coordinates) != len(quadrature):
            raise ValueError('quadrature must have same number of components as coordinates: ' + str(len(quadrature)) + ' ' + str(len(coordinates)))
        self.coordinates = coordinates
        self.quadrature = quadrature

    def getCoordinates(self):
        return self.coordinates

    def getQuadrature(self):
        return self.quadrature

    def show(self):
        print self.coordinates, self.quadrature
    
    
class IndependentMapper:
    def __init__(self, quadratureChooser):
        self.quadratureChooser = quadratureChooser
    def __call__(self, coordinates):
        coorsAndQuad = nestedMap(coordinates, self.quadratureChooser)
        points = map(lambda cAQ: SinglePhasePoint(cAQ[0], cAQ[1]), coorsAndQuad)
        return IndependentList(points)
    
class IndependentList:
    def __init__(self, points):
        self.points = points
    def getPoints(self):
        return self.points
    def getMultiPhasePoints(self):# group the points by coordinates
        hashT = {}
        hashFunc = lambda x: tuple(x.getCoordinates())# replaced in this version ....
        def adder(point):
            hashValue = hashFunc(point)
            if hashT.has_key(hashValue):
                cPoint = hashT[hashValue]
                cPoint.addQuadrature(point.quadrature)
            else:
                newCPoint = sc.MultiPhasePoint(point.coordinates)
                newCPoint.addQuadrature(point.quadrature)
                hashT[hashValue] = newCPoint
        for x in self.points:
            adder(x)
        return hashT.values()
    def newInstance(self, points):
        return IndependentList(points)


class DependentList:
    def __init__(self, points):
        self.points = points
    def getPoints(self):
        return self.points
    def getMultiPhasePoints(self):
        return self.points
    def newInstance(self, points):
        return DependentList(points)
        
class DependentMapper:
    def __init__(self, quadChooser):
        self.quadratureChooser = quadChooser
    def __call__(self, coordinates):
        cPoints = map(lambda coors: sc.MultiPhasePoint(coors, self.quadratureChooser()), coordinates)
        return DependentList(cPoints)
    
        
def nestedMap(points, rangeGenerator):
    return lg.flatmap(lambda point: map(lambda y: [point, y], rangeGenerator()), points)

