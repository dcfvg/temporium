'''
Created on 11 mai 2014

@author: ensadlab
'''
import threading
import time

class AQ_emptying(threading.Thread):
    '''
    thread to run to start a filling AQ with BU, but do not call it directly, use current_state.set_current_action
    '''
    def __init__(self,a_current_state, EL_name):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)

        self.current_state = a_current_state
        self.EL_name = EL_name
        self.action_name = "AQ_emptying_EL_"+EL_name
        
    def run(self):
        self.current_state._set_current_action_aquarium(self.action_name,True)
        self.current_state.set_state_pump("P_AQ_S", True)
        while self.current_state.get_state_EL("AQ",self.EL_name ) and self.current_state.get_current_action_aquarium(self.action_name) : 
            time.sleep(1)
        self.current_state.set_state_pump("P_AQ_S", False) 
        self.current_state._set_current_action_aquarium(self.action_name,False)
        
        