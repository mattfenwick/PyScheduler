'''
Created on Feb 16, 2011

@author: mattf
'''
import unittest
import Halton as h
import Utilities as u
import PoissonDisk as p
import HyperTable as ht
import PoissonGap as pg
import Dispatcher as disp


class HaltonTest(unittest.TestCase):
    
    def setUp(self):
        self.params = {"ranges": [myRange(1, 30),
                                  myRange(1, 30)], 
                        "genPoints": 225}
        self.ranges = self.params['ranges']
        gen = h.getGenerator(self.ranges, self.params['genPoints'])
        self.points = gen()

    def testBounds(self):
        (a,b) = [(min(r), max(r)) for r in self.ranges]
        (mins, maxes) = zip(a,b)
        for pt in self.points:
            zipped = zip(mins, maxes, pt)
            for x in zipped:
                (low, high, c) = x
                self.assertTrue(c >= low)
                self.assertTrue(c <= high, x)
        
    def testNumPointsGenerated(self):
        l1 = len(self.points)
        l2 = self.params['genPoints']
        self.assertEqual(l1, l2, "incorrect number of points generated -- got " + str(l1) + ", wanted " + str(l2))



class HyperTableTest(unittest.TestCase):
    
    def setUp(self):
        self.params = {"ranges": [myRange(1, 30),
                                  myRange(1, 30)]}
        self.ranges = self.params['ranges']
        gen = ht.getGenerator(self.ranges)
        self.points = gen()
    def testXBounds(self):
        (xmin, xmax) = (min(self.ranges[0]), max(self.ranges[0]))
        self.assertTrue(all([x >= xmin and x <= xmax for (x,_) in self.points]), "x coordinates not within boundaries")
    def testYBounds(self):
        (ymin, ymax) = (min(self.ranges[1]), max(self.ranges[1]))
        self.assertTrue(all([y >= ymin and y <= ymax for (_,y) in self.points]), "y coordinates not within boundaries")
    def testNumberOfPoints(self):
        ranges = self.params['ranges']
        gen = ht.getGenerator(ranges)
        points = gen()
        self.assertEqual(len(points),reduce(lambda x,y: x * y, [len(x) for x in ranges], 1), "bad number of points generated")
    def testUniquePoints(self):
        self.assertEqual(len(self.points), len(set([tuple(pt) for pt in self.points])), "repeated points")



class PoissonDiskTest(unittest.TestCase):        
    def setUp(self):
        self.params = {"ranges": [myRange(3, 63),
                                  myRange(3, 53)]}
        self.ranges = self.params['ranges']
        self.gen = p.getGenerator(self.ranges)
        self.points = self.gen()
          
    def testBounds(self):
        (a,b) = [(min(r), max(r)) for r in self.ranges]
        (mins, maxes) = zip(a,b)
        for pt in self.points:
            zipped = zip(mins, maxes, pt)
            for x in zipped:
                (low, high, c) = x
                self.assertTrue(c >= low)
                self.assertTrue(c <= high, x)
                
    def testBoundsLarge(self):
        ranges = [myRange(17,79), myRange(-15, 28)]
        gen = p.getGenerator(ranges)
        points = gen()
        (a,b) = [(min(r), max(r)) for r in ranges]
        (mins, maxes) = zip(a,b)
        for pt in points:
            zipped = zip(mins, maxes, pt)
            for x in zipped:
                (low, high, c) = x
                self.assertTrue(c >= low)
                self.assertTrue(c <= high, x)
                
    def testPointOnLowX(self):
        self.assertTrue(any([x == min(self.ranges[0]) for (x,_) in self.points]), "point on low x boundary")
#        print max([y for (_,y) in self.points])
#        print self.ranges
    def testPointOnLowY(self):
        self.assertTrue(any([y == min(self.ranges[1]) for (_,y) in self.points]), "point on low y boundary")
    def testPointOnHighX(self):
        self.assertTrue(any([x == max(self.ranges[0]) for (x,_) in self.points]), "point on high x boundary")
    def testPointOnHighY(self):
        self.assertTrue(any([y == max(self.ranges[1]) for (_,y) in self.points]), "point on high y boundary")
 

       
class PoissonGapTest(unittest.TestCase):
    def setUp(self):
        self.low = -4
        self.high = 51
        self.numPoints = 34
        gen = pg.getGenerator(self.low, self.high, self.numPoints)
        self.points = gen()
        
    def testBounds(self):
        myBool = all([c[0] >= self.low and c[0] <= self.high for c in self.points])
        self.assertTrue(myBool, "points not within boundaries")

    def testBoundsBig(self):
        (low, high) = 1, 10000
        points = pg.getGenerator(low, high, 283)()
        myBool = all([c[0] >= low and c[0] <= high for c in points])
        self.assertTrue(myBool, "points not within boundaries -- bigger example")
        
    def testNumberOfPoints(self):
        self.assertEqual(len(self.points), self.numPoints, "incorrect number of points generated")
    
    def testTooManyPoints(self):
        (low, high) = 1, 100
        points = pg.getGenerator(low, high, 500)()
        self.assertEqual(len(points), 500, "incorrect number of points generated")



class DispatcherTest(unittest.TestCase):
    def setUp(self):
        self.dim = {'range': [1,100]}
        self.imps = disp.generators.getKeys()
        self.params = {'numGeneratedPoints': 65, 'offsetAngle': 5,
                       'radiusStep': .1, 'angleMultiplier': 1,
                       'gapAngle': 15, 'maximumDeviation': .5,
                       'shellSpacing': 10}
    def testDispatcherInterface(self):
        pass
    def testBuildGenerators1d(self):
        self.params['dimensions'] = [self.dim]
        for i in self.imps:
            if i in ('poissondisk', 'spiral', 'radial'):
                continue
            self.params['coordinateGenerator'] = i
            _ = disp.getObject(self.params)
    def testBuildGenerators2d(self):
        self.params['dimensions'] = [self.dim, self.dim]
        for i in self.imps:
            if i == 'poissongap':
                continue
            self.params['coordinateGenerator'] = i
            _ = disp.getObject(self.params)
    def testBuildGenerators3d(self):
        self.params['dimensions'] = [self.dim, self.dim, self.dim]
        for i in ['hypertable', 'halton']:
            self.params['coordinateGenerator'] = i
            _ = disp.getObject(self.params)
    def testRunGenerators1d(self):
        self.params['dimensions'] = [self.dim]
        for i in self.imps:
            if i in ('poissondisk', 'spiral', 'radial'):
                continue
            self.params['coordinateGenerator'] = i
            g = disp.getObject(self.params)
            points = g()
            [(p[0] + 1) for p in points]
    def testRunGenerators2d(self):
        self.params['dimensions'] = [self.dim, self.dim]
        for i in self.imps:
            if i == 'poissongap':
                continue
            self.params['coordinateGenerator'] = i
            g = disp.getObject(self.params)
            points = g()
            [(p[0] + 1 + p[1]) for p in points]
    def testRunGenerators3d(self):
        myDim = {'range': [1,25]}
        self.params['dimensions'] = [myDim, myDim, myDim]
        for i in ['hypertable', 'halton']:
            self.params['coordinateGenerator'] = i
            g = disp.getObject(self.params)
            points = g()
            [(p[0] + 1 + p[1] + p[2]) for p in points]
    def testGetModules(self):
        modules = disp.getImplementingModules()
        self.assertTrue(len(modules) > 0, "there are no modules implementing the interface")
    def testGetModuleDocs(self):
        modules = disp.getImplementingModules()
        for mod in modules:
            doc = mod.__doc__
            self.assertTrue( doc != None and doc != "", "can't find module documentation")#??
    



def getSuite():
    suite1 = unittest.TestLoader().loadTestsFromTestCase(HyperTableTest)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(HaltonTest)
    suite3 = unittest.TestLoader().loadTestsFromTestCase(PoissonDiskTest)
    suite4 = unittest.TestLoader().loadTestsFromTestCase(PoissonGapTest)
    suite5 = unittest.TestLoader().loadTestsFromTestCase(DispatcherTest)
    return unittest.TestSuite([suite1, suite2, suite3, suite4, suite5])
    
    
def myRange(low, high):
    return u.rangeIncludingBounds(low, high)
