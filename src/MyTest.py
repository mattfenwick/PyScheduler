'''
Created on Feb 16, 2011

@author: mattf
'''

import json as j
import MainFile as mf


myFile = open('test.txt', 'r')
params = j.load(myFile)
mf.getScheduleFromJsonObject(params, "myTestSchedule.txt", True)

#params['coordinateGenerator'] = 'hypertable'

#mf.getScheduleFromJsonObject(params, "exp_random_128_128.txt", True)
