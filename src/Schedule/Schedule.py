'''
Created on Feb 12, 2011

@author: Matt
'''

version = 0.01


class MultiPhasePoint:
    def __init__(self, coords, quadratures = None):
        self.coordinates = coords
        self.quadratures = {}
        if quadratures != None:
            for quad in quadratures:
                self.addQuadrature(quad)

    def addQuadrature(self, quadrature):
        if len(quadrature) != len(self.coordinates):
            raise ValueError("quadrature must have one component for each dimension of MultiPhasePoint")
        #if self.quadratures.has_key(tuple(quadrature)):
        #   raise ValueError("already has quadrature: " + str(quadrature) + ' ' + str(self.coordinates))
        else:
            self.quadratures[tuple(quadrature)] = 1

    def getCoordinates(self):
        return self.coordinates

    def getQuadratures(self):
        return self.quadratures

    def show(self):
        print self.coordinates, self.quadratures
        
    def toJSONObject(self):
        myHash = {"coordinates" : self.coordinates,
                  "quadratures" : self.quadratures.keys()
                  }
        return myHash


class SampleSchedule:
    def __init__(self, multiPhasePoints):#should get all MultiPhasePoints ....
        for x in multiPhasePoints:
            if not isinstance(x, MultiPhasePoint):
                raise TypeError("SampleSchedule should only be getting multi-phase-points: got " + str(type(x)))
        self.points = multiPhasePoints

    def show(self):
        print 'schedule:'
        for x in self.points:
            x.show()

    def getPoints(self):
        return self.points
    
    def toJSONObject(self):
        pointList = [point.toJSONObject() for point in self.points]
        return {"type" : "schedule",
                "version" : version,
                "points" : pointList}

