'''
Created on Feb 14, 2011

@author: mattf
'''
import Bruker as b
import Toolkit as t
import Varian as v
import logging
import Utilities as u
import toJson as tj


def getObject(params):
    myLogger = logging.getLogger("formatter")
    myLogger.debug("determing requested type of formatter....")
    myLogger.debug("parameters used: " + str(params))
    type = params['formatter'] # determine the type of the formatter
    myLogger.debug("coordinate generator type (" + type + ") found, attempting to find formatting module")
    (constructor, _) = formatters[type] # look-up the formatter's module
    myLogger.debug("formatting module found, attempting to get formatting method")
    myPrinter = constructor(params) # get the formatting method from the module
    myLogger.debug("formatting method successfully found")
    return myPrinter


def getBruker(params):
    return b.getPrinter


def getToolkit(params):
    useQuad = params["formatQuadrature"]
    return t.getPrinter(useQuad)


def getVarian(params):
    useQuad = params["formatQuadrature"]
    return v.getPrinter(useQuad)


def getJSON(params):
    return tj.getPrinter



implementingModules = {'bruker':    (getBruker, b),
                       'toolkit':   (getToolkit, t),
                       'varian':    (getVarian, v),
                       'json':      (getJSON, tj)}


def getImplementingModules():
    return [module for (_, module) in implementingModules.values()]

formatters = u.WrappedDictionary(errorMessage = "no such formatter", 
                                 dictionary = implementingModules,
                                 enumeratedParameter = "formatter")
