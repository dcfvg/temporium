'''
Created on 11 mai 2014

@author: ensadlab
'''
import time
from com_arduino import *
from current_state import *

class aquarium_controller(object):
    '''
    manage the aquarium
    '''


    def __init__(self, un_current_state):
        '''
        Constructor
        '''
        self.current_state = un_current_state
    
    def aquarium_recycle_light(self, case):
        """recycle less that 1% of the aquarium at the end of each film"""
        
        if case == 1 :
            """start filtration"""
            print("Start Filtration")
            self.current_state.filter_aquarium(True)
            
            print("Lift Down")
            """lift Down"""
            self.current_state.liftDown()
            """test"""
            time.sleep(1)
            print("Lift Down end")
            
            """emptying AQ for 30 sec"""
            self.emptying_AQ_sec(3)
            
            """get the BU in use"""
            BU_use = self.get_BRBU_USE()
            print("BU in use : "+ BU_use)
            """Filling with BU in USE until AQ is full"""
            self.filling_BU_EL_AQ(str(BU_use))
        
            
            print("Lift Up")
            """lift Up"""
            self.current_state.liftUp()
            time.sleep(10)
            print("Lift Up end")
            
            print("Stop Filtration")
            """stop filtration"""
            self.current_state.filter_aquarium(False)
        
            
        if case == 2 :
            
            """start filtration"""
            print("Start Filtration")
            self.current_state.filter_aquarium(True)

            """emptying AQ for 30 sec"""
            self.emptying_AQ_sec(30)
            
            """get the BU in use"""
            BU_use = self.get_BRBU_USE()
            
            """Filling with BU in USE until AQ is full"""
            self.filling_BU_EL_AQ( BU_use)
            
            print("Lift Down")
            """lift Down"""
            self.current_state.liftDown()
            """test"""
            time.sleep(10)
            print("Lift Down end")
            
            print("Lift Up")
            """lift Up"""
            self.current_state.liftUp()
            time.sleep(10)
            print("Lift Up end")
            
            print("Stop Filtration")
            """stop filtration"""
            self.current_state.filter_aquarium(False)
        

    
    
    def aquarium_recycle_normal(self, case):
        """recycle 10% of the aquarium at the end of each film"""
        
        if case == 1 :
            
            """start filtration"""
            print("Start Filtration")
            self.current_state.filter_aquarium(True)
            
            print("Lift Down")
            """lift Down"""
            self.current_state.liftDown()
            """test"""
            time.sleep(1)
            print("Lift Down end")
            
            """emptying AQ until EL_MEDIUM"""
            self.emptying_AQ_EL()
            
            """get the BU in use"""
            BU_use = self.get_BRBU_USE()
            
            """action to do depending on the formation rate of the image"""
            self.filling_BU_concentration(BU_use, self.get_AQ_concentration())
            
            
            print("Lift Up")
            """lift Up"""
            self.current_state.liftUp()
            time.sleep(10)
            print("Lift Up end")
            
            print("Stop Filtration")
            """stop filtration"""
            self.current_state.filter_aquarium(False)
            
        if case == 2 :
            
            """start filtration"""
            print("Start Filtration")
            self.current_state.filter_aquarium(True)
            
            
            """emptying AQ until EL_MEDIUM"""
            self.emptying_AQ_EL()
            
            """get the BU in use"""
            BU_use = self.get_BRBU_USE()
            
            """action to do depending on the formation rate of the image"""
            self.filling_BU_concentration(BU_use, self.get_AQ_concentration())
            
            
            print("Lift Down")
            """lift Down"""
            self.current_state.liftDown()
            """test"""
            time.sleep(10)
            print("Lift Down end")
            
            print("Lift Up")
            """lift Up"""
            self.current_state.liftUp()
            time.sleep(10)
            print("Lift Up end")
            
            print("Stop Filtration")
            """stop filtration"""
            self.current_state.filter_aquarium(False)
    
    def get_BRBU_USE(self):
        """get the BU in USE state"""
        for item in self.current_state._BRBU_state : 
            if self.current_state.get_BRBU_state(item) == "USE" : 
                return item
    
    def filling_BU_concentration(self, BU_use, AQ_concentration):
        print("filling AQ with BU_USE depending on AQ_concentration")
        pass
    
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
            
        
    def emptying_AQ_EL(self):
        """emptying AQ until EL_AQ_MEDIUM LOW"""
        """be sure that EL is connected"""
        if not self.current_state.get_state_EL("AQ", "MEDIUM" ) == "NULL" : 
            print("emptying AQ until EL_AQ_MEDIUM")
            self.current_state.P_AQ_S(True)
            while self.current_state.get_state_EL("AQ", "MEDIUM" ) :
                    time.sleep(0.05)    
            self.current_state.P_AQ_S(False)
        else : 
            print( "EL_AQ_MEDIUM not connected")
        
       
if __name__ == "__main__":
    com_ard = com_arduino()
    cu_state = current_state(com_ard)
    aq_cont = aquarium_controller(cu_state)
    
    aq_cont.aquarium_recycle_light(1)
        