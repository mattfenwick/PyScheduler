'''
Created on Feb 12, 2011

@author: matt

algorithm:
    print increments of sampling points, one increment per line.  Thus, a single two-dimensional point
    will span two lines, while a three-dimensional point will span three lines.
    This does not print quadrature.  This is one-indexed:  the coordinates of the 'first' point are ones.
    
example (two-dimensional):
1
1
3
5
3
50
5
9

The first point is (1,1), the second is (3,5), etc.
'''


def getPrinter(schedule):
    def pFunc(point):
        return str(reduce(lambda x,y: str(x) + "\n" + str(y) + "\n", point.getCoordinates()))
    return ''.join(map(pFunc, sorted(schedule.getPoints(), key = lambda x: tuple(x.getCoordinates()))))
