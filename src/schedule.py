

class NonUniform(object):
    """
    non-uniform in time, quadrature, transients
    """

    def __init__(self, dims, points):
        self.dims = dims
        self.points = {}
        for p in points:
            self.add(p)

    def add(self, point):
        """example point: ((1, 'R'), (2, 'I'))"""
        if len(point) != self.dims:
            raise ValueError('point size does not match schedule number of dimensions')
        for (c, q) in point:
            if not q in 'RI':
                raise ValueError('invalid quadrature phase -- %' % str(q))
        if not point in self.points:
            self.points[point] = 0
        self.points[point] += 1
    
    def toJSONObject(self):
        return {
            "type" : "NonUniform",
            "dims" : self.dims,
            "points" : [list(map(list, p)) for p in self.points.iteritems()]
        }



class NonUniformTime(object):
    """
    non-uniform in time increments only
    """

    def __init__(self, dims, points):
        self.dims = dims
        self.points = set([])
        for p in points:
            self.add(p)

    def add(self, point):
        """example point: [1, 2]"""
        if len(point) != self.dims:
            raise ValueError('point size does not match schedule number of dimensions')
        if point in self.points:
            raise ValueError("can't add duplicate point to NonUniformTime schedule")
        self.points.add(point)
    
    def toJSONObject(self):
        return {
            "type" : "NonUniformTime",
            "dims" : self.dims,
            "points" : list(self.points)
        }


