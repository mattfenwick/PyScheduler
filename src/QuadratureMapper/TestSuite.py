'''
Created on Mar 26, 2011

@author: mattf
'''
import unittest
import AllPhasesDependent as apd
import AllPhasesIndependent as api
import SingleRandom as sr
import JustReals as jr
import FirstRandomSecondBoth as fsb
import Dispatcher as disp
import random
import logging

myLogger = logging.getLogger("quadratureMapperTest")

rand = random.randint

class DependentQuadratureBase(unittest.TestCase):
    def setUp(self):
        points = []
        if self.dimensions == 1:
            for _ in range(0, 1000):
                points.append((rand(1,10000),))
        elif self.dimensions == 2:
            for _ in range(0, 1000):
                points.append((rand(1,100), rand(1, 100)))
        elif self.dimensions == 3:
            for _ in range(0, 1000):
                points.append((rand(1,100), rand(1, 100), rand(1, 10)))
#        print points
        self.points = set(points)
        self.qPointList = self.gen(self.points)
        self.qPoints = self.qPointList.getPoints()
    def testNumberOfPoints(self):
        expected = len(self.points)
        self.assertEqual(expected, len(self.qPoints))
    def testNoPointsAddedOrRemoved(self):
        qPointSet = set([pt.getCoordinates() for pt in self.qPoints])
        self.assertEqual(set([]), qPointSet.symmetric_difference(self.points))
    def testNumberOfQuadratures(self):
        for pt in self.qPoints:
            quads = pt.getQuadratures()
            self.assertEqual(self.expectedQuadratures, len(quads))
    def testAllQuadraturesUnique(self):
        for pt in self.qPoints:
            quads = pt.getQuadratures()
            self.assertEqual(len(set(quads)), len(quads))
    def testQuadratureDimensions(self):
        for pt in self.qPoints:
            for quad in pt.getQuadratures():
                self.assertTrue(all([q in ['R', 'I'] for q in quad]), 
                                "quadrature dimension has incorrect value: " + str(q))
    def testQuadratureValues(self):
        pass
    def testNumberOfMultiPhasePoints(self):
        mpPoints = self.qPointList.getMultiPhasePoints()
        self.assertEqual(len(mpPoints), len(self.points), 
                         "wrong number of multi-phase points")
    def testQuadratureOfMultiPhasePoints(self):
        mpPoints = self.qPointList.getMultiPhasePoints()
        for pt in mpPoints:
            quads = pt.getQuadratures()
            self.assertTrue(len(quads) >= 1, "point with no quadrature")
            for quad in quads:
                self.assertTrue(all([q in ['R', 'I'] for q in quad]), 
                                "quadrature dimension has incorrect value: " + str(q))
    def __init__(self, dimensions, generator, *args):
        self.dimensions = dimensions
        self.expectedQuadratures = 2 ** self.dimensions
        self.gen = generator
        unittest.TestCase.__init__(self, *args)
            


class AllPhasesDependent1DTest(DependentQuadratureBase):
    def __init__(self, *args):
        dims = 1
        builder = apd.getGenerator(1)
        DependentQuadratureBase.__init__(self, dims, builder, *args)
    
class AllPhasesDependent2DTest(DependentQuadratureBase):
    def __init__(self, *args):
        dims = 2
        builder = apd.getGenerator(2)
        DependentQuadratureBase.__init__(self, dims, builder, *args)
            
class AllPhasesDependent3DTest(DependentQuadratureBase):
    def __init__(self, *args):
        dims = 3
        builder = apd.getGenerator(3)
        DependentQuadratureBase.__init__(self, dims, builder, *args)
    


class SingleRandom1DTest(DependentQuadratureBase):
    def __init__(self, *args):
        dims = 1
        builder = sr.getGenerator(1)
        DependentQuadratureBase.__init__(self, dims, builder, *args)
        self.expectedQuadratures = 1
    
class SingleRandom2DTest(DependentQuadratureBase):
    def __init__(self, *args):
        dims = 2
        builder = sr.getGenerator(2)
        DependentQuadratureBase.__init__(self, dims, builder, *args)
        self.expectedQuadratures = 1

class SingleRandom3DTest(DependentQuadratureBase):
    def __init__(self, *args):
        dims = 3
        builder = sr.getGenerator(3)
        DependentQuadratureBase.__init__(self, dims, builder, *args)
        self.expectedQuadratures = 1

    

class JustReals1DTest(DependentQuadratureBase):
    def __init__(self, *args):
        dims = 1
        builder = jr.getGenerator(1)
        DependentQuadratureBase.__init__(self, dims, builder, *args)
        self.expectedQuadratures = 1

class JustReals2DTest(DependentQuadratureBase):
    def __init__(self, *args):
        dims = 2
        builder = jr.getGenerator(2)
        DependentQuadratureBase.__init__(self, dims, builder, *args)
        self.expectedQuadratures = 1

class JustReals3DTest(DependentQuadratureBase):
    def __init__(self, *args):
        dims = 3
        builder = jr.getGenerator(3)
        DependentQuadratureBase.__init__(self, dims, builder, *args)
        self.expectedQuadratures = 1

    

class FirstRandomSecondBoth2DTest(DependentQuadratureBase):
    def __init__(self, *args):
        dims = 2
        builder = fsb.getGenerator(2)
        DependentQuadratureBase.__init__(self, dims, builder, *args)
        self.expectedQuadratures = 1

    
    
class IndependentQuadratureBase(DependentQuadratureBase):
    def testNumberOfPoints(self):
        expected = 2 ** self.dimensions * len(self.points)
        self.assertEqual(expected, len(self.qPoints))
    def testNumberOfQuadratures(self):
        pass
    def testAllQuadraturesUnique(self):
        pass
    def testQuadratureDimensions(self):
        for pt in self.qPoints:
            quad = pt.getQuadrature()
            self.assertTrue(all([q in ['R', 'I'] for q in quad]), 
                            "quadrature dimension has incorrect value")
    

class AllPhasesIndependent1DTest(IndependentQuadratureBase):
    def __init__(self, *args):
        dims = 1
        builder = api.getGenerator(1)
        DependentQuadratureBase.__init__(self, dims, builder, *args)

class AllPhasesIndependent2DTest(IndependentQuadratureBase):
    def __init__(self, *args):
        dims = 2
        builder = api.getGenerator(2)
        DependentQuadratureBase.__init__(self, dims, builder, *args)

class AllPhasesIndependent3DTest(IndependentQuadratureBase):
    def __init__(self, *args):
        dims = 3
        builder = api.getGenerator(3)
        DependentQuadratureBase.__init__(self, dims, builder, *args)



class DispatcherTest(unittest.TestCase):
    def setUp(self):
        self.dim = {'range': [1, 20]}
        self.params = {'dimensions': [self.dim]}
        self.mappers2d = ['justReals', 'singleRandom', 'allPhasesDependent',
                        'allPhasesIndependent', 'firstRandomSecondBoth']
        self.mappers1d = self.mappers3d = self.mappers2d[0:4]
        self.points1d = set([(rand(1,100),) for _ in range(100)])
        self.points2d = set([(rand(1,100), rand(1,20)) for _ in range(100)])
        self.points3d = set([(rand(1,100), rand(1,20), rand(1,20)) for _ in range(100)])
    def testBuildMappers1D(self):
        for mapper in self.mappers1d:
            self.params['quadratureMapper'] = mapper
            disp.getObject(self.params)
    def testBuildMappers2D(self):
        self.params['dimensions'] = [self.dim, self.dim]
        for mapper in self.mappers2d:
            self.params['quadratureMapper'] = mapper
            disp.getObject(self.params)
    def testBuildMappers3D(self):
        self.params['dimensions'] = [self.dim, self.dim, self.dim]
        for mapper in self.mappers3d:
            self.params['quadratureMapper'] = mapper
            disp.getObject(self.params)
    def testRunMappers1D(self):
        for mapper in self.mappers1d:
            self.params['quadratureMapper'] = mapper
            myMapper = disp.getObject(self.params)
            qPointList = myMapper(self.points1d)
            points = qPointList.getPoints()
            qPointList.getMultiPhasePoints()
            qPointList.newInstance(points[1:14])
    def testRunMappers2D(self):
        self.params['dimensions'] = [self.dim, self.dim]
        for mapper in self.mappers2d:
            self.params['quadratureMapper'] = mapper
            myMapper = disp.getObject(self.params)
            qPointList = myMapper(self.points2d)
            points = qPointList.getPoints()
            qPointList.getMultiPhasePoints()
            qPointList.newInstance(points[1:14])
    def testRunMappers3D(self):
        self.params['dimensions'] = [self.dim, self.dim, self.dim]
        for mapper in self.mappers3d:
            self.params['quadratureMapper'] = mapper
            myMapper = disp.getObject(self.params)
            qPointList = myMapper(self.points3d)
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
    suite = [makeClassSuite(AllPhasesDependent1DTest),
             makeClassSuite(AllPhasesDependent2DTest),
             makeClassSuite(AllPhasesDependent3DTest),
             makeClassSuite(SingleRandom1DTest),
             makeClassSuite(SingleRandom2DTest),
             makeClassSuite(SingleRandom3DTest),
             makeClassSuite(JustReals1DTest),
             makeClassSuite(JustReals2DTest),
             makeClassSuite(JustReals3DTest),
             makeClassSuite(AllPhasesIndependent1DTest),
             makeClassSuite(AllPhasesIndependent2DTest),
             makeClassSuite(AllPhasesIndependent3DTest),
             makeClassSuite(FirstRandomSecondBoth2DTest),
             makeClassSuite(DispatcherTest)]
    return unittest.TestSuite(suite)

if __name__ == "__main__":
    mySuite = getSuite()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
    unittest.main()

