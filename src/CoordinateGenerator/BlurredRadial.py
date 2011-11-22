'''
Created on Mar 31, 2011

@author: mattf
'''
import Radial as rad
import random as r


def getGenerator(ranges, blurWidth, offsetAngle, gapAngle, maximumDeviation):
    xmin, ymin = min(ranges[0]), min(ranges[1])
    xmax, ymax = max(ranges[0]), max(ranges[1])
    xw, yw = xmax - xmin, ymax - ymin
    points = rad.getGenerator(ranges, offsetAngle, gapAngle, maximumDeviation)()
    blurredPoints = []
    for (x,y) in points:
        (xbump, ybump) = myRand(blurWidth), myRand(blurWidth)
        nx, ny = xbump + x, ybump + y
        if nx < xmin:
            continue
#            nx = nx + xw
        elif nx > xmax:
            nx = nx - xw
        if ny < ymin:
            continue
#            ny = ny + yw
        elif ny > ymax:
            ny = ny - yw
        blurredPoints.append((nx, ny))
    blurredSet = set(blurredPoints)
    return lambda: blurredSet
        


def myRand(width):
    return r.randint(-width, width)
