from operator import concat
import math
import random



def blurred(blur_width, points):
    '''
    algorithm:
        adjust all of the points a small, randomly chosen amount in each dimension.
        example:
            blur width = 2,  (x,y) = [3, 7]
            blurx, blury = -1, 2
            blurred = [3 + (-1), 7 + 2] = [2, 9]
    '''
    return [bump_point(pt, blur_width) for pt in points]

def bump_point(coors, blur_width):
    return [bump(c, blur_width) for c in coors]

def bump(c, width):
    return c + random.randint(-width, width)



def bursty(points):
    '''
    algorithm:
        for each point in the given collection of points, select additional adjacent points.  
        This results in an increase in the total number of points.
        In each dimension, either the two adjacent points or no extra points are selected,
        based on a random 50/50 choice.  Thus, in three dimensions, either 0, 2, 4, or 6 
        additional points may be selected.
        
    notes:
        may contain duplicates.  may contain points outside intended bounds
    '''
    return reduce(concat, map(make_adjacent_points, points))

def make_adjacent_points(point):
    all_ = itertools.product(*[make_range(c) for c in point])
    return [pt for pt in all_ if distance(myCoors, pt) <= 1]

def make_range(c):
    if random.randint(0, 1) == 0:
        return [c - 1, c, c + 1]
    else:
        return [c]

def distance(a, b):
    return math.sqrt(sum([(c - d) ** 2 for (c, d) in zip(a, b)]))

