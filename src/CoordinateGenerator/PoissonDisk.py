'''
@author: matt

required parameters:
    number of dimensions
    
algorithm:
    generates a sequence of 2-dimensional points according to the Poisson Disk algorithm
    (uses Herman Tulleken's implementation on http://devmag.org.za/2009/05/03/poisson-disk-sampling/)
    
limitations:  only works for 2-dimensional points
'''
from poisson.poisson_disk import sample_poisson_uniform



def getGenerator(ranges):
    if len(ranges) != 2:
        raise ValueError("poisson disk only works in 2 dimensions")
    return PoissonGenerator(ranges[0], ranges[1])


class PoissonGenerator:
    def __init__(self, rangeX, rangeY, r = 2, k = 30):
        self.ranges = [rangeX, rangeY]
        self.r = r # arbitrary
        self.k = k # arbitrary
        
    def __call__(self):
        ranges = self.ranges
        scalingFactors = [max(x) - min(x) for x in ranges]
        shifts = [min(x) for x in ranges]
        return self.shiftPoints(self.getPoints(scalingFactors[0] + 1, scalingFactors[1] + 1), shifts)
    
    def getPoints(self, x, y):
        poiss = sample_poisson_uniform(x, y, self.r, self.k)
        return [(int(x), int(y)) for (x,y) in poiss]
    
    def shiftPoints(self, points, shifts):
        return [(x + shifts[0], y + shifts[1]) for (x, y) in points]
    
    def setK(self, k):
        self.k = k