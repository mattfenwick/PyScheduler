import json


def varian(formatQuadrature, schedule): # boolean
    '''
    required parameters:
        print quadrature (true -> output will include quadrature, false -> output will include coordinates only)

    algorithm:
        print increments of sampling points, one quadrature component per line.  If no quadrature components are
        printed, then all quadrature components are implicitly assumed to be collected.
        This is zero-indexed:  the coordinates of the 'first' point are zeroes.
        
    example (two-dimensional):
     0 0 II
     0 0 IR
     0 0 RI
     0 0 RR
     2 4 II
     2 4 IR
     2 4 RI
     2 4 RR
     2 49 II
     2 49 IR
     2 49 RI
     2 49 RR
     
    The first point is (0,0); all four quadrature components will be collected.

    example 2 (same as above, but without quadrature):
     0 0
     2 4
     2 49

    '''
    def pFunc(point):
        coordinates = reduce(lambda x,y: str(x) + " " + str(y), map(lambda x: x - 1, point.getCoordinates()), '')
        if formatQuadrature:
            joinedQs = map(lambda x: ''.join(x), sorted(point.getQuadratures()))
            lines = map(lambda quad: coordinates + " " + quad, joinedQs)
            return '\n'.join(lines)
        else: # don't need to print out the quadrature
            return coordinates
    return '\n'.join(map(pFunc, sorted(schedule.getPoints(), key = lambda x: tuple(x.getCoordinates()))))


def toolkit(formatQuadrature, schedule): # boolean
    '''
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


def toJSON(schedule):
    '''
    algorithm:
        the schedule will be formatted as a JSON-compatible text string.
        The exact definition of this format is incomplete.  The output is one-indexed (i.e. first point would be (1,1)).
        
    example:
        please add an illustrative example
    '''
    myJSONObject = schedule.toJSONObject()
    myJSON = json.dumps(myJSONObject)
    return myJSON


def bruker(schedule):
    '''
    algorithm:
        print increments of sampling points, one increment per line.  Thus, a single two-dimensional point
        will span two lines, while a three-dimensional point will span three lines.
        This does not print quadrature.  This is one-indexed:  the coordinates of the 'first' point are ones.
        
    example (two-dimensional):
    1
    1
    3
    5

    The first point is (1,1), the second is (3,5), etc.
    '''
    def pFunc(point):
        return str(reduce(lambda x,y: str(x) + "\n" + str(y) + "\n", point.getCoordinates()))
    return ''.join(map(pFunc, sorted(schedule.getPoints(), key = lambda x: tuple(x.getCoordinates()))))

