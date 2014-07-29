'''
Created on Jun 6, 2014

@author: Cactus
'''
import threading
class spectro(object):
    '''
    classdocs
    '''


    def __init__(self, a_current_state):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        self.current_state = a_current_state
        
    
        