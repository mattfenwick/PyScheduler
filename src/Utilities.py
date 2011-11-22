'''
Created on Feb 16, 2011

@author: mattf
'''
import logging

def rangeIncludingBounds(low, high):
    if high < low:
        raise ValueError("low value of range must be <= high value of range (got " + str(low) + " and " + str(high) + " for low and high)")
    return range(low, high + 1)


class WrappedDictionary:
    """Provides a similar interface as that of the standard python dictionary for getting and setting
    values, but provides a helpful error message with context if a lookup fails."""
    
    def __getitem__(self, name):
        try:
            value = self.dict[name]
            return value
        except:
            message = self.message + ": <" + name + ">"
            if self.enumeratedParameter:
                message += "   please choose one of <" + reduce(lambda x,y: str(x) + " " + str(y), self.dict.keys(), '') + \
                    " > for parameter <" + self.enumeratedParameter + ">"
            logging.error(message)
            raise ValueError(message)
    
    def __setitem__(self, name, value):
        self.dict[name] = value
        
    def __init__(self, errorMessage, dictionary = {}, enumeratedParameter = None):
        self.dict = dictionary
        self.message = errorMessage
        self.enumeratedParameter = enumeratedParameter
        
    def __repr__(self):
        return str(self.dict)
    
    def getKeys(self):
        return self.dict.keys()
