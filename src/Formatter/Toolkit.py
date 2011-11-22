'''
Created on Feb 12, 2011

@author: matt

algorithm:
    print increments of sampling points, one point per line.  All quadrature components are printed on the 
    same line with the coordinates.  
    This is one-indexed:  the coordinates of the 'first' point are ones.
    
example (two-dimensional):
1 1 II IR RI RR
3 5 II IR RI RR
3 50 II IR RI RR
5 9 II IR RI RR
8 19 II IR RI RR
8 65 II IR RI RR
9 35 II IR RI RR
15 1 II IR RI RR

The first point is (1,1) with all four quadrature components.

example (no quadrature):
1 1
3 5
3 50
5 9
'''

def getPrinter(formatQuadrature): # boolean
    def printer(schedule):
        def pFunc(point):
            coordinates = str(reduce(lambda x,y: str(x) + " " + str(y), point.getCoordinates()))
            joinedQs = map(lambda x: ''.join(x), sorted(point.getQuadratures()))
            quadratures = reduce(lambda x,y: str(x) + " " + str(y), joinedQs, '')
            if formatQuadrature:
                return coordinates + quadratures + "\n"
            else:
                return coordinates + "\n"
    #    oldResult = reduce(concat, map(pFunc, sorted(schedule.getPoints(), key = lambda x: tuple(x.getCoordinates()))), '')
        sortedPoints = sorted(schedule.getPoints(), key = lambda x: tuple(x.getCoordinates()))
        newResult = ''.join([pFunc(pt) for pt in sortedPoints])
        return newResult
    return printer
