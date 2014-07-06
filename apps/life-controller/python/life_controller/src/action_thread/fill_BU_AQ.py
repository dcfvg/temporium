'''
Created on 11 mai 2014

@author: ensadlab
'''
import threading
import time

class fill_BU_AQ(threading.Thread):
    '''
    thread to run to start a filling AQ with BU, but do not call it directly, use current_state.set_current_action
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
        self.action_name = "fill_"+self.BU_name+"_AQ"
        
    def run(self):
        
        if False : 
            self.current_state._set_current_action(self.action_name,True)
            print(self.action_name +" start") 
            """alternate between BU->FI and FI-> AQ, and FI-> AQ, to avoid accumulation in FI"""
            compt = 0
            while self.current_state.get_current_action(self.action_name)  : 
                time.sleep(1)
                if compt < 10 : 
                    self.current_state.set_state_pump(self.pump_name,True)
                    self.current_state.P_FI_AQ_1(True)
                    self.current_state.P_FI_AQ_3(True)
                else :
                    self.current_state.set_state_pump(self.pump_name,False)
                    self.current_state.P_FI_AQ_1(True)
                    self.current_state.P_FI_AQ_3(True)
                if compt ==20 : 
                    compt = 0 
                compt = compt + 1
            print("end AQ_filtration")
            self.current_state.set_state_pump(self.pump_name,False)
            self.current_state.P_FI_AQ_1(False)
            self.current_state.P_FI_AQ_3(False)
            self.current_state._set_current_action(self.action_name,False)
            
    

        
        