'''
Created on Mar 8, 2011

@author: mattf
'''

import Display.GraphTest as g
import ToolkitReader as t


def myTest(file):
    opened = open(file, "r")
    text = opened.read()
    sched = t.getSchedule(text)
    g.displayPoints(sched, 128, 128)
    

def myReader():
    myTest("mySched.txt")
#    myTest("myJythonSchedule.txt")
    

myReader()