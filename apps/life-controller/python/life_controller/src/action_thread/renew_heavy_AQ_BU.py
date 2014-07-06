'''
Created on 12 mai 2014

@author: ensadlab
'''
import time 
import threading 

class renew_heavy_AQ_BU(threading.Thread):
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
        self.volume_emptying_AQ = self.current_state.config_manager.get_AQ("VOLUME_TO_EMPTY_HEAVY")
        """get instruction for filling : in shape : [[0.0, 5.0, 0.6], [-5.0, 0.0, 0.7]"""
        self.instruction_filling = self.current_state.config_manager.get_AQ("INSTRUCTION_FILLING")
        self.optimal_concentration= self.current_state.config_manager.get_AQ("CONCENTRAION_OPT")
        
        """ get value of BU_empty""" 
        self.BU_empty =  self.current_state.config_manager.get_BRBU_controller("BU_EMPTY")
        
        
    def run(self):
        
        if self.current_state.get_client_connected("server_level_AQ") and self.current_state.get_client_connected("server_concentration")  :
            self.current_state.set_information_asked("level_AQ", True) 
            
            self.current_state._set_current_action_evolved("renew_heavy_AQ_" + self.BU_use, True)
            """screen down"""
            self.current_state.set_current_action_lift_screen("screen_down_outside")
            """wait until lift_down is finished"""
            while self.current_state.get_lift_busy()  :  
                time.sleep(2)
                
            self.emptying_AQ(self.volume_emptying_AQ)
            self.filling_BU_AQ(self.BU_use)
            
            """screen down"""
            self.current_state.set_current_action_lift_screen("screen_up_outside")
            """wait until lift_down is finished"""
            while self.current_state.get_lift_busy()  :  
                time.sleep(2)
                
            self.current_state._set_current_action_evolved("renew_heavy_AQ_" + self.BU_use, False)
            
            self.current_state.set_information_asked("level_AQ", False)
        else : 
            print ("server_level_AQ or server_concentration not connected")
                                        
    
    
    def emptying_AQ(self, volume):
        if self.current_state.get_client_connected("server_level_AQ") :
            """emptying AQ for sec secondes"""
            print("emptying AQ until " + str(volume))
            
            self.current_state.set_state_pump("P_AQ_S",True)
             
            while self.current_state.get_occupied_volume("AQ") > volume and self.current_state.get_current_action_evolved("renew_heavy_AQ_"+self.BU_use): 
                time.sleep(1)
                
            self.current_state.set_state_pump("P_AQ_S",False)
            print("end emptying AQ")
        
    
    def filling_BU_AQ(self, BU_use):
        """Filling with BU in USE until AQ is full"""
        """be sure that server_level_AQ is connected"""
        if self.current_state.get_client_connected("server_level_AQ") :
            
            """start the spectro and wait for a value"""
            current_concentration = self.current_state.get_spectro_mesure()
            
            """determine volume to fill with BU"""
            volume_to_reach_with_BU = self.det_volume_to_fill_BU(current_concentration)
            
            print("Filling AQ with BU in USE until AQ is full or until a Stop ")
            self.current_state.fill_BU_AQ(BU_use, True)
            """fill until AQ full or stop"""
            while self.current_state.get_occupied_volume("AQ")< volume_to_reach_with_BU and \
                  self.current_state.get_current_action_evolved("renew_heavy_AQ_"+self.BU_use) and \
                  self.current_state.get_occupied_volume (self.BU_use) > self.BU_empty :

                time.sleep(0.05)
            self.current_state.fill_BU_AQ(BU_use, False)
            
            
            """completion with M2"""
            self.current_state.set_state_pump("P_M2_AQ", True)
            while self.current_state.get_occupied_volume("AQ")< self.AQ_FULL and self.current_state.get_current_action_evolved("renew_heavy_AQ_"+self.BU_use): 
                time.sleep(0.05)
            self.current_state.set_state_pump("P_M2_AQ", False)
            
            
        else : 
            print( "server_level_AQ not connected, it will be impossible to fill AQ after")
    
    def det_volume_to_fill_BU(self,current_concentration ):  
        diff = current_concentration - self.optimal_concentration
        """get the percent of the melange to make for filling AQ"""
        action_filling = 0
        for case in self.instruction_filling : 
            if  diff > case[0] and diff < case[1] :
                action_filling = case[2]
                
        """calcul the volum to reach with BU """
        volume_to_reach_with_BU = (1 - self.volume_emptying_AQ)+ self.volume_emptying_AQ*action_filling
        return volume_to_reach_with_BU
        
        
        
    
