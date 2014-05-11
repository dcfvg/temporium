'''
Created on 12 mai 2014

@author: ensadlab
'''
import time 
import threading 

class renew_aquarium(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, a_current_state,a_Bu_use, name):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        self.current_state = a_current_state
        self.name = name
        self.BU_use = a_Bu_use
        
    def run(self):
        if self.name == "light" :
            self.emptying_AQ_sec(12)
            self.filling_BU_EL_AQ(self.BU_use)
        if self.name == "heavy" : 
            pass
            
    
    
    def emptying_AQ_sec(self, sec):
        """be sure that EL HIGH is connected, otherwise it will be impossible to fill the AQ"""
        if not self.current_state.get_state_EL("AQ","HIGH")=="NULL" :  
        
            """emptying AQ for sec secondes"""
            print("emptying AQ for " + str(sec) + " secondes")
            """emptying AQ 30sec"""
            self.current_state.P_AQ_S(True)
            time.sleep(sec)
            self.current_state.P_AQ_S(False)
            print("end emptying AQ")
        else : 
            print( "EL_AQ_HIGH not connected, it will be impossible to fill AQ after")
    
    def filling_BU_EL_AQ(self, BU_use):
        """Filling with BU in USE until AQ is full"""
        """be sure that EL is connected"""
        if not self.current_state.get_state_EL("AQ","HIGH")=="NULL" : 
            
            print("Filling AQ with BU in USE until AQ is full")
            self.current_state.fill_BU_AQ(BU_use, True)
            while not self.current_state.get_state_EL("AQ","HIGH") : 
                time.sleep(0.05)
                
            self.current_state.fill_BU_AQ(BU_use, False)
        else : 
            print ("EL_AQ_MEDIUM not connected") 
        