'''
Created on Feb 12, 2011

@author: matt

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

def getPrinter(formatQuadrature): # boolean
    def printer(schedule):
        def pFunc(point):
            coordinates = reduce(lambda x,y: str(x) + " " + str(y), map(lambda x: x - 1, point.getCoordinates()), '')
            if formatQuadrature:
                joinedQs = map(lambda x: ''.join(x), sorted(point.getQuadratures()))
                lines = map(lambda quad: coordinates + " " + quad, joinedQs)
                return '\n'.join(lines)
            else: # don't need to print out the quadrature
                return coordinates
        return '\n'.join(map(pFunc, sorted(schedule.getPoints(), key = lambda x: tuple(x.getCoordinates()))))
    return printer
