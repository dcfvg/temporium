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
        
        """get parameter"""
        self.AQ_FULL = self.current_state.config_manager.get_AQ("FULL")
        
        """time in second for emptying AQ, load the value at the beginning"""
        self.time_emptying_AQ = self.current_state.config_manager.get_renew_light_AQ("TIME")
        
    def run(self):
        
        if self.current_state.get_client_connected("server_level_AQ") : 
            
            self.current_state._set_current_action_evolved("renew_light_AQ_" + self.BU_use, True)
            """pump AQ->S for 12 sec"""
            self.emptying_AQ_sec(self.time_emptying_AQ)
            self.filling_BU_AQ(self.BU_use)
            self.current_state._set_current_action_evolved("renew_light_AQ_" + self.BU_use, False)
            
            
        else : 
            print( "server_level_AQ not connected, it will be impossible to fill AQ after")
            
    
    
    def emptying_AQ_sec(self, sec):
        if self.current_state.get_client_connected("server_level_AQ") :
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
        
    
    def filling_BU_AQ(self, BU_use):
        """Filling with BU in USE until AQ is full"""
        """be sure that server_level_AQ is connected"""
        if self.current_state.get_client_connected("server_level_AQ") :
            
            
            self.current_state.set_current_action_lift_screen("screen_down_outside")
            """wait until lift_down is finished"""
            while self.current_state.get_lift_busy()  :  
                time.sleep(2)
                
            self.current_state.set_information_asked("level_AQ", True)
            
            print("Filling AQ with BU in USE until AQ is full or until a Stop ")
            self.current_state.fill_BU_AQ(BU_use, True)
            """fill until AQ full or stop"""
            while self.current_state.get_occupied_volume("AQ")< self.AQ_FULL and self.current_state.get_current_action_evolved("renew_light_AQ_"+self.BU_use): 
                time.sleep(0.05)
            self.current_state.fill_BU_AQ(BU_use, False)
            self.current_state.set_information_asked("level_AQ", False)
            
            self.current_state.set_current_action_lift_screen("screen_up_outside")
            """wait until lift_down is finished"""
            while self.current_state.get_lift_busy()  :  
                time.sleep(2)
        else : 
            print( "server_level_AQ not connected, it will be impossible to fill AQ after")
            
    
