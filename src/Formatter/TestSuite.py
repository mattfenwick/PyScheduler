'''
Created on Mar 27, 2011

@author: mattf
'''
import unittest
import Bruker as br
import Varian as va
import Toolkit as tk
import toJson as js
import Dispatcher as disp
import re


class FormatterBase(unittest.TestCase):
    def testLinesMatchRegex(self):
        pass
    def testCanFormatSchedule(self):
        pass
    def testReturnsString(self):
        pass#formatted = self.formatter(schedule)
    def __init__(self, regex, formatter):
        self.regex = regex
        self.formatter = formatter
    
    
class ToolkitTest(FormatterBase):
    def __init__(self, *args):
        regex = re.compile('(?:\d+ ){1,}')# crappy ... and what about quadrature?
        FormatterBase.__init__(self, *args)
        
    
    
    
class DispatcherTest(unittest.TestCase):
    def testBuildFormatters1D(self):
        pass
    def testRunFormatters1D(self):
        pass
    def testGetModules(self):
        modules = disp.getImplementingModules() 
        self.assertTrue(len(modules) > 0, "there are no modules implementing the interface")
    def testGetModuleDocs(self):
        modules = disp.getImplementingModules()
        for mod in modules:
            doc = mod.__doc__
            self.assertTrue( doc != None and doc != "", "can't find module documentation")#??

