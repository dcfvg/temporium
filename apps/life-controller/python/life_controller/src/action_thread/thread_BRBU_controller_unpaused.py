'''
Created on Jul 7, 2014

@author: Cactus
'''

import time 
import threading 

class thread_BRBU_controller_unpaused(threading.Thread):
    
    def __init__(self, a_current_state):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        self.current_state = a_current_state
        
        """try to unpaused every x seconds""" 
        self.wait_time_before_try = 3
        
    def run(self):
        print ("start trying to unpaused every " + str(self.wait_time_before_try) + " seconds")
        while (not self.current_state.get_information_asked("level") )and self.current_state.get_BRBU_controller_state("run") :
            """try to unpaused"""
            time.sleep(self.wait_time_before_try)
            """wait x seconds"""
            self.current_state.set_information_asked("level", True)
              
        self.current_state.set_BRBU_controller_state("pause", False)
            
        print ("BRBU_cycle unpaused")
        