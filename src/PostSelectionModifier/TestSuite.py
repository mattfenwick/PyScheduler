'''
@author: mattf
'''
import unittest as un
import Blurred as bl
import Bursty as bu


# want to test
# for all:
#    all points within boundaries
#    no repeated points (by coordinates)
#    if initial point outside boundaries, new points can also be outside boundaries ....
#
# for blurred:
#    no more points than before
#    all new ones close to old one of same quadrature
#   
# for bursty:
#   all the original points still there
#   no new points not adjacent to an old one
#   new ones have same quadratures as old ones from which they came

class ModifierBase(un.TestCase):
    def testPointsWithinBoundaries(self):
        coordinates = [pt.getCoordinates() for pt in self.newPoints]
        for coor in coordinates:
            zipped = zip(coor, self.rangeLists)# [1, 2] and [[1, 128], [1, 128]] -> [(1, [1, 128]), (2, [1, 128])]
            for (c, (high, low)) in zipped:
                self.assertTrue(low <= c <= high, "new point within boundaries")
    def testNoRepeatedCoordinates(self):
        coordinates = [tuple(pt.getCoordinates()) for pt in self.newPoints]
        coordinateSet = set(coordinates)
        self.assertEqual(len(coordinates), len(coordinateSet), "coordinates of each point is unique")
    


class TestBursty(ModifierBase):
    def setUp(self):
        pass
    def testAllOriginalPointsPresent(self):
        pass
    def testAllNewPointsAdjacentToOriginalPoint(self):
        self.assertTrue(False, "test not implemented")
    


class TestBlurred(ModifierBase):
    def setUp(self):
        pass
    def testNumberOfPoints(self):
        pass
    def testAllNewPointsCloseToOriginalPoint(self):
        self.assertTrue(False, "test not implemented")
    



def makeClassSuite(myClass):
    return un.TestLoader().loadTestsFromTestCase(myClass)
    
def getSuite():
    suite = [makeClassSuite(c) for c in [TestBursty, TestBlurred]]
    return un.TestSuite(suite)

if __name__ == "__main__":
    mySuite = getSuite()
    un.TextTestRunner(verbosity=2).run(mySuite)
#    unittest.main()

