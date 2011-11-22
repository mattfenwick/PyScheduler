'''
Created on Mar 17, 2011

@author: mattf
'''

try:
    import json as j # if standard library module fails to load,
except Exception, e:
    import myJSON as j # use my poor replacement
    import logging
    logging.warning("couldn't load python standard library module json: " + e.message + " ... switching to myJSON")
    
    
dumps = j.dumps

load = j.load

