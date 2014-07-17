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
        
        """wait time after asking level information"""
        self._time_wait_webcam = self.current_state.config_manager.get_webcam("time_wait")
        
    def run(self):
        print ("start trying to unpaused every " + str(self._time_wait_webcam) + " seconds")
        while (not self.current_state.get_information_asked("level") )and self.current_state.get_BRBU_controller_state("run") :
            """try to unpaused"""
            time.sleep(self._time_wait_webcam)
            """wait x seconds"""
            self.current_state.set_information_asked("level", True)
           
        time.sleep(self._time_wait_webcam)
        self.current_state.set_BRBU_controller_state("pause", False)
            
        print ("BRBU_cycle unpaused")
        