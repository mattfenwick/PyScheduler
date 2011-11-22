'''
Created on Feb 15, 2011

@author: mattf
'''
coordinateGenerators = set('halton', 'hypertable', 'poissondisk', 'poissongap')
formatters = set('varian', 'toolkit', 'bruker')
pointSelectors = set()
quadratureMappers = set()
forcedSelectors = set()


class DimensionParameters:
    def __init__(self, myRange = [0, 60], decayRate = 60,
                 sweepWidth = 8000, exponent = 1):
        self.setRange(myRange)
        self.setDecayRate(decayRate)
        self.setSweepWidth(sweepWidth)
        self.setExponent(exponent)
    def setRange(self, myRange):
        try:
            if myRange[1] > myRange[0]:
                self.myRange = range(myRange[0], myRange[1])
            else:
                raise ValueError
        except:
            raise ValueError("dimension.range needs a low and a high as a list: [low, high]")
    def setDecayRate(self, decayRate):
        try:
            if decayRate > 0:
                self.decayRate = decayRate
            else:
                raise ValueError
        except:
            raise ValueError("dimension.decayRate needs a positive number")
    def setSweepWidth(self, sweepWidth):
        try:
            if sweepWidth > 0:
                self.sweepWidth = sweepWidth
            else:
                raise ValueError
        except:
            raise ValueError("dimension.sweepWidth needs a positive number")
    def setExponent(self, exponent):
        try:
            exponent + 1#should raise exception if not number
        except:
            raise ValueError("dimension.exponent needs a number")


class SamplingParameters:
    def __init__(self, coordinateGenerator = "hypertable", formatter = "toolkit",
                 pointSelector = "exponential", quadratureMapper = "allPhasesDependent",
                 numSelectedPoints = 400, forcedSelector = "allWithZero",
                 dimensions = [DimensionParameters(), DimensionParameters()],
                 numGeneratedPoints = None):
        self.setCGen(coordinateGenerator)
        self.setForm(formatter)
        self.setPSel(pointSelector)
        self.setQMap(quadratureMapper)
        self.setNumSelectedPoints(numSelectedPoints)
        self.setForcedSelector(forcedSelector)
        self.setDimensions(dimensions)
        self.setNumGeneratedPoints(numGeneratedPoints)
        
    def setCGen(self, cGen):
        if cGen in coordinateGenerators:
            self.coordinateGenerator = cGen
        else:
            raise ValueError("invalid coordinate generator")
        
    def setForm(self, formatter):
        if formatter in formatters:
            self.formatter = formatter
        else:
            raise ValueError("invalid formatter")
        
    def setPSel(self, pSel):
        if pSel in pointSelectors:
            self.pointSelector = pSel
        else:
            raise ValueError("invalid point selector")
        
    def setQMap(self, quadratureMapper):
        if quadratureMapper in quadratureMappers:
            self.quadratureMapper = quadratureMapper
        else:
            raise ValueError("invalid quadrature mapper")
        
    def setNumSelectedPoints(self, num):
        if num > 0:
            self.numSelectedPoints = num
        else:
            raise ValueError("numSelectedPoints must be a positive number")
        
    def setForcedSelector(self, forcedSelector):
        if forcedSelector in forcedSelectors:
            self.forcedSelector = forcedSelector
        else:
            raise ValueError("invalid forcedSelector")
        
    def setDimensions(self, dimensions):
        for dim in dimensions:
            if not isinstance(dim, DimensionParameters):
                raise ValueError("dimensions must be instances of DimensionParameters")
        self.dimensions = dimensions
            
    def setNumGeneratedPoints(self, ):
        pass
    
x = {
    "coordinateGenerator": "hypertable",
        
    "numGeneratedPoints": 400,
     
    "formatter": "toolkit", 
    
    "pointSelector": "exponential",
     
    "quadratureMapper": "justReals",
    
    "numSelectedPoints" : 400,
    
    "forcedSelector" : "allWithZero",
        
    "dimensions": 
        [
            {"range": [0, 90], "decayRate": 60, "sweepWidth": 8000, "exponent" : 1}, 
            {"range": [0, 90], "decayRate": 60, "sweepWidth": 8000, "exponent" : 1}
        ]
}