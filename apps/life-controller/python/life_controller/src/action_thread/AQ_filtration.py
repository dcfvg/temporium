'''
Created on 11 mai 2014

@author: ensadlab
'''
import threading
import time

class AQ_filtration(threading.Thread):
    '''
    thread to run to start a filtration of AQ, but do not call it directly, use current_state.set_current_action
    '''

    def __init__(self,a_current_state):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)

        self.current_state = a_current_state
        
        self.action_name = "AQ_filtration"
        
        
        
    def run(self):
        self.current_state._set_current_action(self.action_name,True)
        print("Filtration AQ start") 
        """alternate between AQ->FI and FI-> AQ, and FI-> AQ, to avoid accumulation in FI"""
        compt = 0
        while self.current_state.get_current_action(self.action_name)  : 
            time.sleep(1)
            if compt < 10 : 
                self.current_state.P_AQ_FI(True)
                self.current_state.P_FI_AQ_1(True)
                self.current_state.P_FI_AQ_3(True)
            else :
                self.current_state.P_AQ_FI(False)
                self.current_state.P_FI_AQ_1(True)
                self.current_state.P_FI_AQ_3(True)
            if compt ==20 : 
                compt = 0 
            compt = compt + 1
        print("end "+ self.action_name )
        self.current_state.P_AQ_FI(False)
        self.current_state.P_FI_AQ_1(False)
        self.current_state.P_FI_AQ_3(False)
        self.current_state._set_current_action(self.action_name,False)
        
        
        
        
    

        
        