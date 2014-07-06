'''
Created on 11 mai 2014

@author: ensadlab
'''
import threading
import time

class empty_BU_S(threading.Thread):
    '''
    thread to run to start a emptying BU in S, but do not call it directly, use current_state.set_current_action
    NOT USE 
    '''


    def __init__(self,a_current_state, a_BU_name):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)

        self.BU_name = a_BU_name
        self.current_state = a_current_state
        
        """set the name of the pump, and the name of the action asked"""
        self.pump_name = "P_" + self.BU_name+"_FI"
        self.action_name = "empty_"+self.BU_name+"_S"
        
    def run(self):
        if False : 
            self.current_state._set_current_action(self.action_name,True)
            print(self.action_name +" start") 
            """alternate between BU->FI and FI-> S, and FI-> S, to avoid accumulation in FI"""
            compt = 0
            while self.current_state.get_current_action(self.action_name)  : 
                time.sleep(1)
                if compt < 10 : 
                    self.current_state.set_state_pump(self.pump_name,True)
                    self.current_state.P_FI_S(True)
                    self.current_state.P_FI_S(True)
                else :
                    self.current_state.set_state_pump(self.pump_name,False)
                    self.current_state.P_FI_S(True)
                    self.current_state.P_FI_S(True)
                if compt ==20 : 
                    compt = 0 
                compt = compt + 1
            print("end BU_empty")
            self.current_state.set_state_pump(self.pump_name,False)
            self.current_state.P_FI_S(False)
            self.current_state.P_FI_S(False)
            self.current_state._set_current_action(self.action_name,False)
            
    

        
        