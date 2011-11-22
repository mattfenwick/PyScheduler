'''
Created on Mar 24, 2011

@author: mattf
'''
import Common
import random


def getGenerator(nDimensions):
    if nDimensions != 2:
        raise ValueError("FirstRandomSecondBoth only works for 2-dimensional runs")
    quads = ['R', 'I']
    length = len(quads)
    def closure():
        myQuad = [quads[random.randint(0, length - 1)], 'B']
        return [myQuad]
    return Common.DependentMapper(closure)