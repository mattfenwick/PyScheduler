'''
Created on Mar 25, 2011

@author: mattf
'''
import unittest
import AllLowerBounds as allLB
import AllWithZero as allWZ
import SelectNone as sn
import PointBlock as pBlock
import Dispatcher as disp


def incRange(l, h):
    """range including high endpoint"""
    return range(l, h + 1)

class AllLowerBoundsTest(unittest.TestCase):
    
    def setUp(self):
        self.xr = [1, 32]
        self.yr = [1, 72]
        self.zr = [1, 103]
        myXRange, yrange, zrange = (incRange(self.xr[0], self.xr[1]), 
                                    incRange(self.yr[0], self.yr[1]), 
                                    incRange(self.zr[0], self.zr[1]))
        self.gen1 = allLB.getSelector([myXRange])
        self.gen2 = allLB.getSelector([myXRange, yrange])
        self.gen3 = allLB.getSelector([myXRange, yrange, zrange])

    def testOnLowerBounds1D(self):
        points = self.gen1()
        self.assertTrue(points[0][0] == self.xr[0], "point not on boundary")
    def testWithinBounds1D(self):
        points = self.gen1()
        xc = points[0][0]
        self.assertTrue(self.xr[0] <= xc <= self.xr[1], "point not within specified range")
    def testNumberOfPoints1D(self):
        self.assertTrue(len(self.gen1()) == 1, "bad number of points")
        
    def testOnLowerBounds2D(self):
        points = self.gen2()
        xlow, ylow = self.xr[0], self.yr[0]
        self.assertTrue(all([x == xlow or y == ylow for (x,y) in points]), "point not on boundary")
    def testWithinBounds2D(self):
        points = self.gen2()
        xlow, xhigh = self.xr
        ylow, yhigh = self.yr
        for (x,y) in points:
            self.assertTrue(xlow <= x <= xhigh, "x not within specified range")
            self.assertTrue(ylow <= y <= yhigh, "y not within specified range")
    def testNumberOfPoints2D(self):
        points = self.gen2()
        myXRange, yrange = (incRange(self.xr[0], self.xr[1]), 
                            incRange(self.yr[0], self.yr[1]))
        expected = len(myXRange) + len(yrange) - 1
        actual = len(points)
        self.assertTrue(actual == expected, "wrong number of points (expected " + 
                        str(expected) + ", got " + str(actual) + ")")
    def testOnLowerBounds3D(self):
        points = self.gen3()
        xlow, ylow, zlow = self.xr[0], self.yr[0], self.zr[0]
        self.assertTrue(all([x == xlow or y == ylow or z == zlow for (x,y,z) in points]), "point not on boundary")
    def testWithinBounds3D(self):
        points = self.gen3()
        xlow, xhigh = self.xr
        ylow, yhigh = self.yr
        zlow, zhigh = self.zr
        for (x,y, z) in points:
            self.assertTrue(xlow <= x <= xhigh, "x not within specified range")
            self.assertTrue(ylow <= y <= yhigh, "y not within specified range")
            self.assertTrue(zlow <= z <= zhigh, "z not within specified range")
    def testNumberOfPoints3D(self):
        points = self.gen3()
        myXRange, yrange, zrange = (incRange(self.xr[0], self.xr[1]), 
                                    incRange(self.yr[0], self.yr[1]),
                                    incRange(self.zr[0], self.zr[1]))
        xlen, ylen, zlen = len(myXRange), len(yrange), len(zrange)
        expected = xlen * ylen + xlen * zlen + ylen * zlen - xlen - ylen - zlen + 1
        actual = len(points)
        self.assertTrue(actual == expected, "wrong number of points (expected " + 
                        str(expected) + ", got " + str(actual) + ")")
    
    
class SelectNoneTest(unittest.TestCase):
    def setUp(self):
        self.gen = sn.getSelector()
    def test1D(self):
        points = self.gen()
        self.assertTrue(len(points) == 0, "iterable is not empty")
    def test2D(self):
        points = self.gen()
        self.assertTrue(len(points) == 0, "iterable is not empty")
    def test3D(self):
        points = self.gen()
        self.assertTrue(len(points) == 0, "iterable is not empty")
        
        
class AllWithZeroTest(unittest.TestCase):
    def setUp(self):
        pass
    
    
class PointBlockTest(unittest.TestCase):
    def setUp(self):
        self.xr = [1, 32]
        self.yr = [1, 72]
        self.zr = [1, 103]
        self.myXRange = incRange(self.xr[0], self.xr[1]) 
        self.yrange = incRange(self.yr[0], self.yr[1]) 
        self.zrange = incRange(self.zr[0], self.zr[1])
        self.gen1 = pBlock.getSelector([self.myXRange])
        self.gen2 = pBlock.getSelector([self.myXRange, self.yrange])
        self.gen3 = pBlock.getSelector([self.myXRange, self.yrange, self.zrange])
    def testAllPointsUnique1D(self):
        points = self.gen1()
        pointSet = set([tuple(pt) for pt in points])
        self.assertTrue(len(points) == len(pointSet), "repeated point")
    def testNoneOutsideRange1D(self):
        points = self.gen1()
        low, high = self.xr
        self.assertTrue(all([low <= x <= high for (x,) in points]), "point not in range")
    def testNumberOfPoints1D(self):
        points = self.gen1()
        self.assertTrue(len(points) == len(self.myXRange), "wrong number of points")
    def testAllPointsUnique2D(self):
        points = self.gen2()
        pointSet = set([tuple(pt) for pt in points])
        self.assertTrue(len(points) == len(pointSet), "repeated point")
    def testNoneOutsideRange2D(self):
        points = self.gen2()
        xl, xh = self.xr
        yl, yh = self.yr
        for x,y in points:
            self.assertTrue(xl <= x <= xh, "point not in x range")
            self.assertTrue(yl <= y <= yh, "point not in y range")
    def testNumberOfPoints2D(self):
        points = self.gen2()
        expected = len(self.myXRange) * len(self.yrange)
        self.assertTrue(len(points) == expected, "wrong number of points")
    def testAllPointsUnique3D(self):
        points = self.gen3()
        pointSet = set([tuple(pt) for pt in points])
        self.assertTrue(len(points) == len(pointSet), "repeated point")
    def testNoneOutsideRange3D(self):
        points = self.gen3()
        xl, xh = self.xr
        yl, yh = self.yr
        zl, zh = self.zr
        for x,y,z in points:
            self.assertTrue(xl <= x <= xh, "point not in x range")
            self.assertTrue(yl <= y <= yh, "point not in y range")
            self.assertTrue(zl <= z <= zh, "point not in z range")
    def testNumberOfPoints3D(self):
        points = self.gen3()
        actual = len(points)
        expected = len(self.myXRange) * len(self.yrange) * len(self.zrange)
        self.assertTrue(actual == expected, "wrong number of points (expected " +
                        str(expected) + ", got " + str(actual) + ")")


class DispatcherTest(unittest.TestCase):
    def setUp(self):
        self.dim = {'range': [1, 100],
                    'blockRange': [1, 15]}
        self.imps = disp.selectors.getKeys()
    def testDispatcherInterface(self):
        pass
    def testBuildSelectors1d(self):
        params = {'dimensions': [self.dim], 'specialHaltonPoints': 20}
        for i in self.imps:
            params['forcedSelector'] = i
            _ = disp.getObject(params)
    def testBuildSelectors2d(self):
        params = {'dimensions': [self.dim, self.dim], 'specialHaltonPoints': 200}
        for i in self.imps:
            params['forcedSelector'] = i
            _ = disp.getObject(params)
    def testBuildSelectors3d(self):
        params = {'dimensions': [self.dim, self.dim, self.dim], 'specialHaltonPoints': 2000}
        for i in self.imps:
            params['forcedSelector'] = i
            _ = disp.getObject(params)
    def testRunSelectors1d(self):
        params = {'dimensions': [self.dim], 'specialHaltonPoints': 20}
        for i in self.imps:
            params['forcedSelector'] = i
            g = disp.getObject(params)
            points = g()
            [(p[0] + 1) for p in points]
    def testRunSelectors2d(self):
        params = {'dimensions': [self.dim, self.dim], 'specialHaltonPoints': 200}
        for i in self.imps:
            params['forcedSelector'] = i
            g = disp.getObject(params)
            points = g()
            [(p[0] + 1 + p[1]) for p in points]
    def testRunSelectors3d(self):
        params = {'dimensions': [self.dim, self.dim, self.dim], 'specialHaltonPoints': 2000}
        for i in self.imps:
            params['forcedSelector'] = i
            g = disp.getObject(params)
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
    suite1 = unittest.TestLoader().loadTestsFromTestCase(AllLowerBoundsTest)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(SelectNoneTest)
    suite3 = unittest.TestLoader().loadTestsFromTestCase(PointBlockTest)
    suite4 = unittest.TestLoader().loadTestsFromTestCase(DispatcherTest)
    return unittest.TestSuite([suite1, suite2, suite3, suite4])

if __name__ == "__main__":
    mySuite = getSuite()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
    #unittest.main()
