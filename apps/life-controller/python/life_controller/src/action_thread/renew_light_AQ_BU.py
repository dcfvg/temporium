'''
Created on 12 mai 2014

@author: ensadlab
'''
import time 
import threading 

class renew_light_AQ_BU(threading.Thread):
    '''
    thread to run to start a filling AQ with BU, but do not call it directly, use current_state.set_current_action
    '''


    def __init__(self, a_current_state,a_Bu_use):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        self.current_state = a_current_state
        self.BU_use = a_Bu_use
        
        """time in second for emptying AQ, load the value at the beginning"""
        self.time_emptying_AQ = self.current_state.config_manager.get_renew_light_AQ("TIME")
        
    def run(self):
        
        if not self.current_state.get_state_EL("AQ","HIGH")=="NULL" : 
            self.current_state._set_current_action_evolved("renew_light_AQ_" + self.BU_use, True)
            """pump AQ->S for 12 sec"""
            self.emptying_AQ_sec(self.time_emptying_AQ)
            self.filling_BU_EL_AQ(self.BU_use)
            self.current_state._set_current_action_evolved("renew_light_AQ_" + self.BU_use, False)
        else : 
            print( "EL_AQ_HIGH not connected, it will be impossible to fill AQ after")
            
    
    
    def emptying_AQ_sec(self, sec):
        if not self.current_state.get_state_EL("AQ","HIGH")=="NULL" :
            """emptying AQ for sec secondes"""
            print("emptying AQ for " + str(sec) + " secondes")
            """emptying AQ 30sec"""
            self.current_state.P_AQ_S(True)
            compt = 0 
            while self.current_state.get_current_action_evolved("renew_light_AQ_"+self.BU_use) and compt <sec : 
                time.sleep(1)
                compt = compt + 1
            self.current_state.P_AQ_S(False)
            print("end emptying AQ")
        
    
    def filling_BU_EL_AQ(self, BU_use):
        """Filling with BU in USE until AQ is full"""
        """be sure that EL is connected"""
        if not self.current_state.get_state_EL("AQ","HIGH")=="NULL" : 
            
            print("Filling AQ with BU in USE until AQ is full or until a Stop ")
            self.current_state.fill_BU_AQ(BU_use, True)
            """fill until AQ full or stop"""
            while not self.current_state.get_state_EL("AQ","HIGH") and self.current_state.get_current_action_evolved("renew_light_AQ_"+self.BU_use): 
                time.sleep(0.05)
            self.current_state.fill_BU_AQ(BU_use, False)
        else : 
            print( "EL_AQ_HIGH not connected, it will be impossible to fill AQ after")
    
