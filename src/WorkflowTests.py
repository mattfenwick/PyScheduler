'''
Created on Mar 28, 2011

@author: mattf
'''
import unittest as un
import MainFile as mf
import sys
import CoordinateGenerator.Dispatcher as cgenD
import SpecialPointSelector.Dispatcher as specD
import QuadratureMapper.Dispatcher as quadD
import PointSelector.Dispatcher as pselD
import Formatter.Dispatcher as formD


baseDim = {'range': [1, 20],
           'blockRange': [1,10],
           'sweepWidth': 8000,
           'decayRate':  164,
           'exponent':  1,
           'probabilityFunction': '1 / i',
           }

baseParams = {'coordinateGenerator': 'halton',
              'forcedSelector':  'none',
              'quadratureMapper': 'singleRandom',
              'pointSelector':    'random',
              'formatter':        'toolkit',
              'numGeneratedPoints': 50,
              'numSelectedPoints':  35,
              'seed': 718,
              'dimensions': [baseDim]
              }


class Results:
    def __init__(self, *args):
        self.values = {}
        for y in args:
            for x in y:
                self.values[x] = {'passed': 0, 'failed': 0}
    def addResult(self, value, result):
        self.values[value][result] += 1
    def show(self):
        print "-------results-----------"
        for x in self.values.keys():
            e = self.values[x]
            print 'value ' + x + ':    failed: ' + str(e['failed']) + '    passed: ' + str(e['passed'])


class Tester(un.TestCase):
    def testAll(self):
        cgens = cgenD.implementingModules.keys()
        specs = specD.implementingModules.keys()
        quads = quadD.implementingModules.keys()
        psels = pselD.implementingModules.keys()
        forms = formD.implementingModules.keys()
        params = baseParams
        results = Results(cgens, specs, quads, psels, forms, [str(x) for x in range(1,4)])
        for c in cgens:
            params['coordinateGenerator'] = c
            for sp in specs:
                params['forcedSelector'] = sp
                for q in quads:
                    params['quadratureMapper'] = q
                    for p in psels:
                        params['pointSelector'] = p
                        if p == "adjustedExponential":
                            continue
                        for f in forms:
                            params['formatter'] = f
                            for dims in [[baseDim], [baseDim, baseDim], [baseDim, baseDim, baseDim]]:
                                if len(dims) != 1 and c == 'poissongap' or q == 'firstRandomSecondBoth' or q == 'FRSBD1Same':
                                    continue
                                if len(dims) != 2 and c == 'poissondisk' or c == 'radial' or c == 'spiral' or c == 'blurredRadial':
                                    continue
                                params['dimensions'] = dims
                                params['seed'] = 718
                                if len(dims) == 1:
                                    params['numSelectedPoints'] = 35
                                    params['numGeneratedPoints'] = 50
                                elif len(dims) == 2:
                                    params['numSelectedPoints'] = 750
                                    params['numGeneratedPoints'] = 2000
                                elif len(dims) == 3:
                                    params['numSelectedPoints'] = 2500
                                    params['numGeneratedPoints'] = 5000
                                name = '_'.join([c, sp, q, p, f, str(len(dims))])
                                myKeys = [c, sp, q, p, f, str(len(dims))]
                                try:
                                    (_, sched) = mf.getScheduleFromJsonObject(params)
                                    points = sched.getPoints()
                                    [(pt.getCoordinates(), pt.getQuadratures()) for pt in points]
                                    print "passed:", name
                                    # want to check whether points right, etc.
                                    for x in myKeys:
                                        results.addResult(x, 'passed')
                                except Exception, e:
                                    sys.stderr.write("problem: " + str(e) + " (test " + name + ")\n") 
                                    for x in myKeys:
                                        results.addResult(x, 'failed')
        results.show()


def makeClassSuite(myClass):
    return un.TestLoader().loadTestsFromTestCase(myClass)
    
#def getSuite():
#    suite = [makeClassSuite(c) for c in [Tester]]
#    return un.TestSuite(suite)

if __name__ == "__main__":
    mySuite = makeClassSuite(Tester)
    un.TextTestRunner(verbosity=2).run(mySuite)

