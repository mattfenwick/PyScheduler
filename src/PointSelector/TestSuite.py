'''
@author: mattf
'''
import unittest
import All
import Exponential as exp
import Randoms as ran
import UserDefined as usd
import Dispatcher as disp
import QuadratureMapper.Common as qc
import random



rand = random.randint

def getPoints1D():
    points = []
    quads = ['R', 'I']
    for _ in range(1000):
        points.append((rand(1, 100000), ) )
    pointSet = set(points)
    initialPoints = [qc.SinglePhasePoint(pt, (quads[rand(0, 1)], )) for pt in pointSet]
    return qc.IndependentList(initialPoints)

def getPoints2D():
    points = []
    quads = ['R', 'I']
    for _ in range(1000):
        points.append((rand(1, 100), rand(1, 100)) )
    pointSet = set(points)
    initialPoints = [qc.SinglePhasePoint(pt, (quads[rand(0, 1)], 
                                              quads[rand(0, 1)])) for pt in pointSet]
    return qc.IndependentList(initialPoints)

def getPoints3D():
    points = []
    quads = ['R', 'I']
    for _ in range(1000):
        points.append((rand(1, 100), rand(1, 10), rand(1, 10)) )
    pointSet = set(points)
    initialPoints = [qc.SinglePhasePoint(pt, (quads[rand(0, 1)], 
                                              quads[rand(0, 1)],
                                              quads[rand(0, 1)])) for pt in pointSet]
    return qc.IndependentList(initialPoints)


class SelectorBase(unittest.TestCase):
    def testNumberOfPoints(self):
        raise Exception("please override this method in a sub-class")
    def testNoNewPoints(self):
        selectedPoints = self.selectedPointList.getPoints()
        originalSet = set(self.initialPoints.getPoints())
        for pt in selectedPoints:
            self.assertTrue(pt in originalSet, "selected point not in original points")
    def testPointListInterface(self):
        spl = self.selectedPointList
        spl.getPoints()
        spl.getMultiPhasePoints()
        spl.newInstance([])
    def testSomeAlreadySelected(self):
        arbitraryNumber = 52
        newList = self.selector(self.initialPoints, arbitraryNumber)
        length = len(newList.getPoints())
        self.assertEqual(self.numToSelect - arbitraryNumber, length)
    def testTooManyPointsAlreadySelected(self):
        arb = 10000
        newList = self.selector(self.initialPoints, arb)
        length = len(newList.getPoints())
        self.assertEqual(0, length)    
    

class Test1D(SelectorBase):
    def setUp(self):
        self.numToSelect = 73
        self.initialPoints = getPoints1D()
        self.selectedPointList = self.selector(self.initialPoints, 0)
    

class Test2D(SelectorBase):
    def setUp(self):
        self.numToSelect = 278
        self.initialPoints = getPoints2D()
        self.selectedPointList = self.selector(self.initialPoints, 0)
    

class Test3D(SelectorBase):
    def setUp(self):
        self.numToSelect = 840
        self.initialPoints = getPoints3D()
        self.selectedPointList = self.selector(self.initialPoints, 0)



class AllTest1D(Test1D):
    def testNumberOfPoints(self):
        self.assertEqual(len(self.selectedPointList.getPoints()), 
                         len(self.initialPoints.getPoints()))
    def setUp(self):
        self.selector = All.getSelector()
        Test1D.setUp(self)
    def testSomeAlreadySelected(self):
        arbitraryNumber = 52
        newList = self.selector(self.initialPoints, arbitraryNumber)
        length = len(newList.getPoints())
        self.assertEqual(len(self.selectedPointList.getPoints()), length)
    testTooManyPointsAlreadySelected = testSomeAlreadySelected



class AllTest2D(Test2D):
    def testNumberOfPoints(self):
        self.assertEqual(len(self.selectedPointList.getPoints()), 
                         len(self.initialPoints.getPoints()))
    def setUp(self):
        self.selector = All.getSelector()
        Test2D.setUp(self)
    def testSomeAlreadySelected(self):
        arbitraryNumber = 52
        newList = self.selector(self.initialPoints, arbitraryNumber)
        length = len(newList.getPoints())
        self.assertEqual(len(self.selectedPointList.getPoints()), length)
    testTooManyPointsAlreadySelected = testSomeAlreadySelected



class AllTest3D(Test3D):
    def testNumberOfPoints(self):
        self.assertEqual(len(self.selectedPointList.getPoints()), 
                         len(self.initialPoints.getPoints()))
    def setUp(self):
        self.selector = All.getSelector()
        Test3D.setUp(self)
    def testSomeAlreadySelected(self):
        arbitraryNumber = 52
        newList = self.selector(self.initialPoints, arbitraryNumber)
        length = len(newList.getPoints())
        self.assertEqual(len(self.selectedPointList.getPoints()), length)
    testTooManyPointsAlreadySelected = testSomeAlreadySelected




class RandomTest1D(Test1D):
    def testNumberOfPoints(self):
        self.assertEqual(len(self.selectedPointList.getPoints()), 
                         self.numToSelect)
    def setUp(self):
        self.numToSelect = 73
        self.selector = ran.getSelector(self.numToSelect)
        Test1D.setUp(self)


class RandomTest2D(Test2D):
    def testNumberOfPoints(self):
        self.assertEqual(len(self.selectedPointList.getPoints()), 
                         self.numToSelect)
    def setUp(self):
        self.numToSelect = 278
        self.selector = ran.getSelector(self.numToSelect)
        Test2D.setUp(self)


class RandomTest3D(Test3D):
    def testNumberOfPoints(self):
        self.assertEqual(len(self.selectedPointList.getPoints()), 
                         self.numToSelect)
    def setUp(self):
        self.numToSelect = 840
        self.selector = ran.getSelector(self.numToSelect)
        Test3D.setUp(self)



class UserDefinedTest1D(Test1D):
    def testNumberOfPoints(self):
        self.assertEqual(len(self.selectedPointList.getPoints()), 
                         self.numToSelect)
    def setUp(self):
        self.numToSelect = 73
        self.selector = usd.getSelector([{'probabilityFunction':"1 / i"}], self.numToSelect)
        Test1D.setUp(self)


class UserDefinedTest2D(Test2D):
    def testNumberOfPoints(self):
        self.assertEqual(len(self.selectedPointList.getPoints()), 
                         self.numToSelect)
    def setUp(self):
        self.numToSelect = 278
        self.selector = usd.getSelector([{'probabilityFunction':"1 / i"}, 
                                         {'probabilityFunction':"i ** 2"}], self.numToSelect)
        Test2D.setUp(self)


class UserDefinedTest3D(Test3D):
    def testNumberOfPoints(self):
        self.assertEqual(len(self.selectedPointList.getPoints()), 
                         self.numToSelect)
    def setUp(self):
        self.numToSelect = 840
        self.selector = usd.getSelector([{'probabilityFunction':"1 / i"}, 
                                         {'probabilityFunction':"i ** 2"}, 
                                         {'probabilityFunction':"i"}], self.numToSelect)
        Test3D.setUp(self)



class ExponentialTest1D(Test1D):
    def testNumberOfPoints(self):
        self.assertEqual(len(self.selectedPointList.getPoints()), 
                         self.numToSelect)
    def setUp(self):
        self.numToSelect = 73
        dim = exp.DimensionParameters()
        params = exp.Parameters([dim])
        self.selector = exp.getSelector(params, self.numToSelect)
        Test1D.setUp(self)


class ExponentialTest2D(Test2D):
    def testNumberOfPoints(self):
        self.assertEqual(len(self.selectedPointList.getPoints()), 
                         self.numToSelect)
    def setUp(self):
        self.numToSelect = 278
        dim = exp.DimensionParameters()
        params = exp.Parameters([dim])
        self.selector = exp.getSelector(params, self.numToSelect)
        Test2D.setUp(self)


class ExponentialTest3D(Test3D):
    def testNumberOfPoints(self):
        self.assertEqual(len(self.selectedPointList.getPoints()), 
                         self.numToSelect)
    def setUp(self):
        self.numToSelect = 840
        dim = exp.DimensionParameters()
        params = exp.Parameters([dim])
        self.selector = exp.getSelector(params, self.numToSelect)
        Test3D.setUp(self)



class DispatcherTest(unittest.TestCase):
    def setUp(self):
        self.dim = {'sweepWidth': 8000, 'decayRate': 164, 'exponent': 1, 'probabilityFunction': '1 / i'}
        self.params = {'numSelectedPoints': 328, 'dimensions': [self.dim]}
        self.Selectors1d = self.Selectors3d = self.Selectors2d = ['exponential', 'userDefined', 'random', 'all']
        self.points1d = getPoints1D()
        self.points2d = getPoints2D()
        self.points3d = getPoints3D()
    def testBuildSelectors1D(self):
        for selector in self.Selectors1d:
            self.params['pointSelector'] = selector
            disp.getObject(self.params)
    def testBuildSelectors2D(self):
        self.params['dimensions'] = [self.dim, self.dim]
        for selector in self.Selectors2d:
            self.params['pointSelector'] = selector
            disp.getObject(self.params)
    def testBuildSelectors3D(self):
        self.params['dimensions'] = [self.dim, self.dim, self.dim]
        for selector in self.Selectors3d:
            self.params['pointSelector'] = selector
            disp.getObject(self.params)
    def testRunSelectors1D(self):
        for selector in self.Selectors1d:
            self.params['pointSelector'] = selector
            myselector = disp.getObject(self.params)
            qPointList = myselector(self.points1d, 0)
            points = qPointList.getPoints()
            qPointList.getMultiPhasePoints()
            qPointList.newInstance(points[1:14])
    def testRunSelectors2D(self):
        self.params['dimensions'] = [self.dim, self.dim]
        for selector in self.Selectors2d:
            self.params['pointSelector'] = selector
            myselector = disp.getObject(self.params)
            qPointList = myselector(self.points2d, 0)
            points = qPointList.getPoints()
            qPointList.getMultiPhasePoints()
            qPointList.newInstance(points[1:14])
    def testRunSelectors3D(self):
        self.params['dimensions'] = [self.dim, self.dim, self.dim]
        for selector in self.Selectors3d:
            self.params['pointSelector'] = selector
            myselector = disp.getObject(self.params)
            qPointList = myselector(self.points3d, 0)
            points = qPointList.getPoints()
            qPointList.getMultiPhasePoints()
            qPointList.newInstance(points[1:14])
    def testGetModules(self):
        modules = disp.getImplementingModules()
        self.assertTrue(len(modules) > 0, "there are no modules implementing the interface")
    def testGetModuleDocs(self):
        modules = disp.getImplementingModules()
        for mod in modules:
            doc = mod.__doc__
            self.assertTrue( doc != None and doc != "", "can't find module documentation")#??

        
def makeClassSuite(myClass):
    return unittest.TestLoader().loadTestsFromTestCase(myClass)
    
def getSuite():
    suite = [makeClassSuite(c) for c in [AllTest1D, AllTest2D, AllTest3D,
                                         RandomTest1D, RandomTest2D, RandomTest3D,
                                         UserDefinedTest1D, UserDefinedTest2D, UserDefinedTest3D,
                                         ExponentialTest1D, ExponentialTest2D, ExponentialTest3D,
                                         DispatcherTest]]
    return unittest.TestSuite(suite)

if __name__ == "__main__":
    mySuite = getSuite()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
#    unittest.main()
