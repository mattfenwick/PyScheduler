'''
Created on Mar 16, 2011

@author: mattf

algorithm:
    the schedule will be formatted as a JSON-compatible text string.
    The exact definition of this format is incomplete.  The output is one-indexed (i.e. first point would be (1,1)).
    
example:
    please add an illustrative example
'''

import jsonWrapper as j
# avoid if necessary json module because Jython is not yet Python2.6 compatible
#import json
#
#
#def getPrinter(schedule):
#    myJSONObject = schedule.toJSONObject()
#    print myJSONObject
#    return json.toJSON(myJSONObject)

def getPrinter(schedule):
    myJSONObject = schedule.toJSONObject()
    myJSON = j.dumps(myJSONObject)
    return myJSON



    
