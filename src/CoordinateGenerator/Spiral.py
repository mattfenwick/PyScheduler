'''
@author: mattf

required parameters:
    per dimension:
    
algorithm:
    
'''
import math as m


def getGeneratorOld(rangeLists):
    a = .05
    b = .1
    ((xl, xh), (yl, yh)) = rangeLists
    def func():
        points = []
        for ang in range(0, 10500):
            theta = 2 * m.pi * ang/ 500
            r = a * m.e ** (b * theta)
            x,y = r * m.cos(theta), r * m.sin(theta)
            x,y = abs(int(x)), abs(int(y))
            points.append((x,y))
        pointSet = set(points)
        ordered = sorted(pointSet)
        filtered = [pt for pt in ordered if xl <= pt[0] <= xh and yl <= pt[1] <= yh ]
        return filtered
    return func


def getGenerator(rangeLists, rstep, angleMultiplier, offsetAngle):
    if len(rangeLists) == 2:
        return getGenerator2D(rangeLists, rstep, angleMultiplier, offsetAngle)
    elif len(rangeLists) == 3:
        return getGenerator3D(rangeLists, rstep, angleMultiplier, offsetAngle)
    else:
        raise ValueError("bad number of dimensions: " + str(len(rangeLists)))
    

def getGenerator2D(rangeLists, rstep, a2, offset):
    points = []
    ((xl, xh), (yl, yh)) = rangeLists
    xspan, yspan = xh - xl, yh - yl
    r = 0
    radianOffset = offset * m.pi / 180
    while r <= m.sqrt(xspan ** 2 + yspan ** 2):
        theta = a2 * r + radianOffset
        x = abs(int(r * m.cos(theta))) + xl
        y = abs(int(r * m.sin(theta))) + yl
        if x <= xh and y <= yh:
            points.append((x, y))
        r = r + rstep
    pointSet = set(points)
    return lambda: pointSet


def getGenerator3D(rangeLists, rstep, a2, b):
    points = []
    ((xl, xh), (yl, yh), (zl, zh)) = rangeLists
    xspan, yspan, zspan = xh - xl, yh - yl, zh - zl
    r = 0
    phiA, phiB = 100, 20
    while r <= m.sqrt(xspan ** 2 + yspan ** 2 + zspan **2):
        theta = a2 * r + b
        phi = phiA * r + phiB
        x = abs(int(r * m.sin(theta) * m.cos(phi))) + xl
        y = abs(int(r * m.sin(theta) * m.sin(phi))) + yl
        z = abs(int(r * m.cos(theta))) + zl
        if x <= xh and y <= yh and z <= zh:
            points.append((x, y, z))
        r = r + rstep
    pointSet = set(points)
    return lambda: pointSet
        
        
