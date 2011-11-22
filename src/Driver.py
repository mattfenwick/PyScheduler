'''
Created on Jan 27, 2011

@author: mattf
'''
import CoordinateGenerator.Dispatcher as c
import QuadratureMapper.Dispatcher as q
import PointSelector.Dispatcher as p
import Formatter.Dispatcher as f
import SpecialPointSelector.Dispatcher as sp
import PostSelectionModifier.Dispatcher as psm
import Schedule.Schedule as sc
import random
import logging


def makeSchedule(parameters):
    seed = parameters['seed']
    random.seed(seed)
    cgen = c.getObject(parameters)  # get the coordinate generator
    spec = sp.getObject(parameters) # get the special point selector
    qmap = q.getObject(parameters)  # get the quadrature mapper
    psel = p.getObject(parameters)  # get the normal point selector
    form = f.getObject(parameters)  # get the formatter
    pmod = psm.getObject(parameters) # get the post-selection-modifier # this is new
    # parameters should now have been fully validated, so that if making the schedule was going to fail, it should already have failed
#    return runScheduleWorkflowTest(cgen, spec, qmap, psel, form) # old one
    return runScheduleWorkflowTestWithPostSelectionModification(cgen, spec, qmap, psel, form, pmod) # this is new



def runScheduleWorkflowTest(cgen, spec, qmap, psel, form):
    myLogger = logging.getLogger("workflow")
    myLogger.debug("starting workflow:  generating coordinates")
    points = cgen()                                                         # generate some coordinates
    myLogger.debug('generated ' + str(len(points)) + ' points')             # see how many were generated
#    mySet = set(points)
#    (l1, l2) = len(mySet), len(points)
    myLogger.debug("selecting special points")
    special = spec() # select special points
    normal = filterSpecialPoints(special, points)                            # make sure no special points are left in the normal pool
    myLogger.debug("selected special points .... points left in normal pool: " + str(len(normal)) + "  specially selected points: " + str(len(special)))
    myLogger.debug("applying quadrature ...")
    (normList, specList) = (qmap(normal), qmap(special))                    # apply quadrature to both the normal pool and the special pool
    myLogger.debug("quadrature applied to normal and special points")
    numAlreadySelected = len(specList.getPoints())                   # number of points that still need to be selected:  original minus number of special points
    myLogger.debug("selecting normal points (" + str(numAlreadySelected) + " already selected)")
    selectedList = psel(normList, numAlreadySelected)                          # select that many points from the normal list
    myLen = len(selectedList.getPoints()) + len(specList.getPoints())       # the number of points selected is the number in the special list plus the number selected from the normal list
    myLogger.debug("selected " + str(myLen) + " points total (special + normal)")
    myLogger.debug("creating sample schedule ...")
    schedule = sc.SampleSchedule(selectedList.getMultiPhasePoints() +       # create a schedule from all the special points and the normally-selected points
                                 specList.getMultiPhasePoints())
    myLogger.debug("sample schedule completed, formatting schedule")
    formatted = form(schedule)                                              # format the schedule as a string
    myLogger.debug("sample schedule formatted")
    return (formatted, schedule)


def filterSpecialPoints(special, points):
    if len(special) == 0:
        return points
    ptSet = set([tuple(pt) for pt in points])
    specialSet = set([tuple(pt) for pt in special])
    return ptSet.difference(specialSet)



def runScheduleWorkflowTestWithPostSelectionModification(cgen, spec, qmap, psel, form, pmod):
    myLogger = logging.getLogger("workflow")
    myLogger.debug("starting workflow:  generating coordinates")
    points = cgen()                                                         # generate some coordinates
    myLogger.debug('generated ' + str(len(points)) + ' points')             # see how many were generated
#    mySet = set(points)
#    (l1, l2) = len(mySet), len(points)
    myLogger.debug("selecting special points")
    special = spec() # select special points
    normal = filterSpecialPoints(special, points)                            # make sure no special points are left in the normal pool
    myLogger.debug("selected special points .... points left in normal pool: " + str(len(normal)) + "  specially selected points: " + str(len(special)))
    myLogger.debug("applying quadrature ...")
    (normList, specList) = (qmap(normal), qmap(special))                    # apply quadrature to both the normal pool and the special pool
    myLogger.debug("quadrature applied to normal and special points")
    numAlreadySelected = len(specList.getPoints())                   # number of points that still need to be selected:  original minus number of special points
    myLogger.debug("selecting normal points (" + str(numAlreadySelected) + " already selected)")
    selectedList = psel(normList, numAlreadySelected)                          # select that many points from the normal list
    myLen = len(selectedList.getPoints()) + len(specList.getPoints())       # the number of points selected is the number in the special list plus the number selected from the normal list
    myLogger.debug("selected " + str(myLen) + " points total (special + normal)")
    allSelectedPoints = selectedList.getMultiPhasePoints() + specList.getMultiPhasePoints()
    myLogger.debug("applying any post-selection modification operators to selected points ...")
    modifiedPoints = pmod(allSelectedPoints)                                # apply any post-selection modifications
    myLogger.debug(str(len(modifiedPoints)) + " points left after applying post-selection modifier ...")
    myLogger.debug("creating sample schedule ...")
    schedule = sc.SampleSchedule(modifiedPoints)                            # create a schedule from all the special points and the normally-selected points
    myLogger.debug("sample schedule completed, formatting schedule")
    formatted = form(schedule)                                              # format the schedule as a string
    myLogger.debug("sample schedule formatted")
    return (formatted, schedule)
