'''
Created on Mar 29, 2011

@author: mattf
'''
import argparse as a
import CoordinateGenerator as cgen
import SpecialPointSelector as spec
import QuadratureMapper as quad
import PointSelector as psel
import Formatter as form
import Testing as t
import Parameters as pars


def main():
    parser = a.ArgumentParser(description = "Get info, run tests on sample scheduler")
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-t', '--test', action='store_const', const=True)
    group.add_argument('-m', '--moduleHelp', action='store_const', const=True)
    group.add_argument('-o', '--overview', action='store_const', const=True)
    args = parser.parse_args()
    if args.test:
        test()
    elif args.moduleHelp:
        printHelp()
    elif args.overview:
        printOverview()
    
    
    
def printHelp():
    for m in [cgen, spec, quad, psel, form]:
        print "package: ", m.__name__, m.Dispatcher.__doc__, "\n=========================================="
        for imp in m.Dispatcher.getImplementingModules():
            print "module: ", imp.__name__
            print imp.__doc__
            print "------------------------------------------\n"
        print "------------------------------------------\n"
    
    
def test():
    t.runTests()
    
    
def printOverview():
    for x in pars.types:
        print "parameter: ", x, "    type: ", pars.types[x].func_name
    for x in pars.dimensionTypes:
        print "dimension parameter: ", x, "    type: ", pars.dimensionTypes[x].func_name
    
    
if __name__ == "__main__":
    main()

