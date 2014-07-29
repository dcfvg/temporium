'''
Created on Jun 5, 2014

@author: Cactus
'''
import time

class time_controller(object):
    '''
    classdocs
 '''
""""
0     tm_year     (for example, 1993)
1     tm_mon     range [1, 12]
2     tm_mday     range [1, 31]
3     tm_hour     range [0, 23]
4     tm_min     range [0, 59]
5     tm_sec     range [0, 61]; 
6     tm_wday     range [0, 6],
7     tm_yday     range [1, 366]
8     tm_isdst"""

print (time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.localtime()))
time.localtime()[1]

    def __init__(selfparams):
        '''
        Constructor
        '''
        