'''
Created on Feb 12, 2011

@author: mattf
'''
import logging
myLogger = logging.getLogger("probabilitySelector")


class ProbabilitySelector:
    def __call__(self, pointList, numAlreadySelected):
        numToSelect = self.totalPoints - numAlreadySelected
        if numToSelect <= 0:
            myLogger.warning("too many points already selected:  needed " + str(self.totalPoints) + 
                             ", but already selected " + str(numAlreadySelected))
            return pointList.newInstance([])
        if numToSelect > len(pointList.getPoints()):
            myLogger.warning("trying to select " + str(numToSelect) + " points but only " + 
                                                             str(len(pointList.getPoints())) + " available")
        selected = selectPointsByProbability(pointList.getPoints(), self.probFunc, numToSelect)
        return pointList.newInstance(selected)

    def __init__(self, probFunc, numTotalToSelect):
        self.probFunc = probFunc
        self.totalPoints = numTotalToSelect
        
        
    
def selectPointsByProbability(points, ampFunc, number):
    probPoints = map(lambda x: [ampFunc(x.getCoordinates()), x], points)
    sortedPoints = sorted(probPoints, key = lambda x: x[0])
    sortedPoints.reverse()
    selected = sortedPoints[:number]
    return map(lambda x: x[1], selected)