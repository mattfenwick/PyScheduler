'''
@author: mattf

required parameters:
    per dimension:
        range (low and high)

algorithm:
    generate coordinates of points, where the points lie along 'spokes' radiating out from the origin
'''
import math as m
import HyperTable as ht



def getGenerator(ranges, offsetAngle, gapAngle, maximumDeviation):
    allPoints = ht.getGenerator(ranges)()
    origin = [r[0] for r in ranges]
    points = [pt for pt in allPoints if myFilter(pt, origin, offsetAngle, gapAngle, maximumDeviation)]
    return lambda: points
    
    
def myFilter(pt, origin, offsetAngle, degreeGap, tolerance):
    y,x = pt[0] - origin[0], pt[1] - origin[1]
    theta = m.atan2(x, y) * 180. / m.pi # angle in degrees
    ratio = (theta + offsetAngle) / degreeGap
    return abs(ratio - round(ratio)) * degreeGap < tolerance