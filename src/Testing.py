'''
Created on Feb 16, 2011

@author: mattf
'''
import CoordinateGenerator.TestSuite as ctest
import SpecialPointSelector.TestSuite as specTest
import QuadratureMapper.TestSuite as quadTest
import PointSelector.TestSuite as selTest
import Formatter.TestSuite as formTest
import PostSelectionModifier.TestSuite as modTest
import unittest
import logging
logging.basicConfig(filename = "logForUnitTests.txt", level = logging.DEBUG, filemode = 'w')


def runTests():
    mySuite = unittest.TestSuite([module.getSuite() for module in [ctest, specTest, quadTest, selTest, modTest]])
    unittest.TextTestRunner(verbosity=2).run(mySuite)
#    unittest.main()

if __name__ == "__main__":
    runTests()