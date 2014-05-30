'''
Created on Apr 29, 2014

@author: glogzy (tete de thon)
'''
import time
from com_arduino import*
from current_state import*
from fake_clock import *

import threading

class BRBU_controller (threading.Thread):

    def __init__ (self, un_current_state):
      
        threading.Thread.__init__ (self, target=self.run)
        

        """self.current_state"""
        self.current_state = un_current_state
        
        """if false, it's the first time it enter in the cycle : work to do then it is ready, True"""
        self.BR_BU_ready = {"BU1" : False , "BU2" : False , "BU3" : False }

        
        """if BU is empty for the EMPTY state"""
        self.BU_empty = {"BU1" : False , "BU2" : False , "BU3" : False }
 
        
        """Empty for BU before EMPTY state"""

        """setcurrent time in hour"""
        
        """if wish to have a fake time"""
        self.fake = False
        
        if self.fake : 
            self.fake_clock = fake_clock(1)
            self.current_time = self.fake_clock.time()/3600
            self.old_time = self.fake_clock.time()/3600       
        else :
            self.current_time = time.time()/3600
            self.old_time = time.time()/3600

        
        
    def run (self):
        
        print("Cycle BRBU will begin in 30 sec")
        time.sleep(30)
        self.current_time = time.time()/3600
        self.old_time = time.time()/3600
        print("debut BRBU")
        while True :
            
            
            """way of knowing time betweeen two round"""
            if self.fake :
                self.current_time = self.fake_clock.time()/3600
            else :
                self.current_time = time.time()/3600
              
           
            """ time betweeen two round in hour"""
            time_laps_hour = (self.current_time - self.old_time) % 216 
            
            """ time betweeen two round in minute"""
            time_laps_minute = (60 * time_laps_hour)%60        
            
            time_laps_second = (60 * time_laps_minute)%216
            
            print("time_sec " + str(time_laps_second))
            
            """1 : WAIT , 2 : USE , 3 : EMPTY, with B1 : WAIT, B2 : USE , B3 : EMPTY"""
            """Day 1 -Day  3  """
            if time_laps_hour < 72 : 
                self.current_state.set_BRBU_state("BU1", "WAIT")
                self.current_state.set_BRBU_state("BU2", "USE")
                self.current_state.set_BRBU_state("BU3", "EMPTY")
                
                self.BR_BU_ready["BU2"] = False
                self.BU_empty["BU1"] = False
    


                """Day 3 -Day  6  """
            elif time_laps_hour < 144 :
                self.current_state.set_BRBU_state("BU1", "USE")
                self.current_state.set_BRBU_state("BU2", "EMPTY")
                self.current_state.set_BRBU_state("BU3", "WAIT")
                
                self.BR_BU_ready["BU1"] = False
                self.BU_empty["BU3"] = False

        
                """Day 6 -Day  9  """
            elif time_laps_hour < 216 :
                self.current_state.set_BRBU_state("BU1", "EMPTY")
                self.current_state.set_BRBU_state("BU2", "WAIT")
                self.current_state.set_BRBU_state("BU3", "USE")
                
                self.BR_BU_ready["BU3"] = False
                self.BU_empty["BU2"] = False
            
            """reset variable"""
            #self.reset()
            
            #for item in self.current_state.BRBU_state : 
              #  print (item + " " + str(self.current_state.get_BRBU_state(item)) )

            """Action on BU - BR to produce alguae"""
            
            """if B1 is in WAIT"""
            if self.current_state.get_BRBU_state("BU1") == "WAIT":
                
                """At the begining of WAIT for C1"""
                if not self.BR_BU_ready["BU1"] :
                    
                    """empty BR and fill BU : 2/3 BR -> BU """
                    
                    while self.current_state.get_occupied_volume("BU1") < 0.66 :
                        self.current_state.P_BR1_BU1(True)
                        """maybe add : if pump is in manuel-mode, end the manuel mode"""
                    self.current_state.P_BR1_BU1(False)
        
                    
                    """fill BU : full with M2 """
                    while self.current_state.get_occupied_volume("BU1") < 1 :
                        self.current_state. P_M2_BU1(True)
                    self.current_state.P_M2_BU1(False)
    
                    
                    """fill BR : full with M1 """
                    while self.current_state.get_occupied_volume("BR1") < 1 :
                        self.current_state.P_M1_BR1(True)  
                    self.current_state.P_M1_BR1(False)   
                    
                    """BR1_BU1_ready ready """
                    self.BR_BU_ready["BU1"] = True;                
            
            
            """if B2 is in WAIT"""
            if self.current_state.get_BRBU_state("BU2") == "WAIT":
                if not self.BR_BU_ready["BU2"] :
                    
                    """empty BR and fill BU : 2/3 BR -> BU """
                    
                    while self.current_state.get_occupied_volume("BU2") < 0.66 :
                        self.current_state.P_BR2_BU2(True)
                    self.current_state.P_BR2_BU2(False)
    
                    
                    """fill BU : full with M2 """
                    while self.current_state.get_occupied_volume("BU2") < 1 :
                        self.current_state. P_M2_BU2(True)
                    self.current_state.P_M2_BU2(False)
    
                    
                    """fill BR : full with M1 """
                    while self.current_state.get_occupied_volume("BR2") < 1 :
                        self.current_state.P_M1_BR2(True)
                    self.current_state.P_M1_BR2(False)   
              
                    """BR2_BU2_ready ready """
                    self.BR_BU_ready["BU2"] = True            
            
            """if B3 is in WAIT"""
            if self.current_state.get_BRBU_state("BU3") == "WAIT" :
                
                if not self.BR_BU_ready["BU2"] :
                    
                    """empty BR and fill BU : 2/3 BR -> BU """
                    while self.current_state.get_occupied_volume("BU3") < 0.66 :
                        self.current_state.P_BR3_BU3(True)
                    self.current_state.P_BR3_BU3(False)
    
                    
                    """fill BU : full with M2 """
                    while self.current_state.get_occupied_volume("BU3") < 1 :
                        self.current_state. P_M2_BU3(True)
                    self.current_state.P_M2_BU3(False)
                    
                    
                    """fill BR : full with M1 """
                    while self.current_state.get_occupied_volume("BR3") < 1 :
                        self.current_state.P_M1_BR3(True)
                    self.current_state.P_M1_BR3(False)   
    
                    
                    """BR_BU_ready ready """
                    self.BR_BU_ready["BU3"] = True;
            
            
            if self.current_state.get_BRBU_state("BU1") == "EMPTY":
                """for testing purposes, emptying BU"""
                if not self.BU_empty["BU1"]  : 
                    
                    """function to complete, action to do at the begining of EMPTY"""
                    
                    while self.current_state.get_occupied_volume("BU1") > 0.1 :
                        self.current_state.fill_BU1_AQ(True)
                    self.current_state.fill_BU1_AQ(False)
                    self.BU_empty["BU1"] = True  
                              
                
            if self.current_state.get_BRBU_state("BU2") == "EMPTY":
                if not self.BU_empty["BU2"]  :
                    """function to complete, action to do at the begining of EMPTY"""
                     
                    while self.current_state.get_occupied_volume("BU2") > 0.1 :
                        self.current_state.fill_BU2_AQ(True)
                    self.current_state.fill_BU2_AQ(False) 
                    self.BU_empty["BU2"] = True 
                        
                        
                
            if self.current_state.get_BRBU_state("BU3") == "EMPTY":
                if not self.BU_empty["BU3"]  :
                    """function to complete, action to do at the begining of EMPTY"""
                    while self.current_state.get_occupied_volume("BU3") > 0.1 :
                        self.current_state.fill_BU3_AQ(True)
                    self.current_state.fill_BU3_AQ(False) 
                    self.BU_empty["BU3"] = True
            
            
            
            time.sleep(1)    
            
    
    def reset(self):
        """function to call to rest BU_empty et BRBU_ready, to do the filling at the right time"""
        for item in self.current_state.BRBU_state : 
            if not self.current_state.get_BRBU_state(item) == "WAIT" : 
                self.current_state.set_BRBU_state(item, False)
                
            if not self.current_state.get_BRBU_state(item) == "EMPTY" : 
                self.BU_empty[item] = False
        
             

   
