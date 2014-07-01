'''
Created on May 24, 2014

@author: Cactus
'''
import threading
import time

class arduino_lift_thread(threading.Thread):
    '''
    thread that check the security electrode_max and stop every process if an EL turns ON (meaning that there is a problem ) 
    '''

    def __init__(self,a_arduino_lift):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)

        self.arduino_lift = a_arduino_lift
        
        self.current_state = self.arduino_lift.com_arduino.current_state
        
        
        """lock to start being busy"""
        self._start_busy = threading.Lock()
        """set to lock at the beginning"""
        self._start_busy.acquire()
        
        self.start()
        
    def run(self):
        
        while True : 
            """release by arduino_lift when starting an action"""
            self._start_busy.acquire()
            #print("start thread")
            self.current_state._set_current_action_lift_screen(self.action_name,True )
            """set arduino_lift_busy_state to True"""
            self.arduino_lift.set_busy_state(True)
            
            self.arduino_lift._is_occupied()
            
            self.arduino_lift.set_busy_state(False)
            self.current_state._set_current_action_lift_screen(self.action_name,False )
            #print("end thread")
        
        
    """launch the busy state"""
    def start_busy(self, action_name):
        self.action_name = action_name
        self._start_busy.release()
    
           
    
        
        
        
        
        
    

        
        
