'''
Created on Jan 23, 2011

@author: mattf
'''

import logging
# what if I want to save the log somewhere else?  because I haven't gotten the cl args yet ....
#    on the other hand, I want to be able to report any import errors
LOG_FILENAME = "myLogger.txt"
logging.basicConfig(filename = LOG_FILENAME, level = logging.DEBUG, filemode = 'w')

import Driver as dr
import jsonWrapper as j
import argparse as a
import Utilities
import Parameters


    
    
def main():
    try:
        parser = a.ArgumentParser(description = "Generate sample schedules")
        parser.add_argument('parameterfile', type=str, help='json formatted file containing parameters used to generate the schedule')
        parser.add_argument('savelocation', type=str, help='location to save the generated schedule')
        args = parser.parse_args()
    
        logging.debug("opening file " + args.parameterfile)
        savepath = args.savelocation
        myFile = open(args.parameterfile, 'r')
        params = j.load(myFile)
        (formatted, _) = getScheduleFromJsonObject(params) # ignore the schedule for now
        logging.debug("writing schedule to file " + savepath)
        outfile = open(savepath, 'w')
        outfile.write(formatted)
        outfile.close()
    except Exception, e:
        logging.error(e)
        raise
        
            
        
def getScheduleFromJsonObject(parameters):
    params = Utilities.WrappedDictionary("missing parameter", parameters)
    Parameters.validateAndMassageParameters(params)
    logging.debug(params)
    (stri, sched) = dr.makeSchedule(params)
    return (stri, sched)
    



if __name__ == "__main__":
    main()

