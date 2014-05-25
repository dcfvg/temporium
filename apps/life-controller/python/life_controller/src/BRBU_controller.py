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
        
        """self.lock to wait for start, release it in order to start"""
        self.lock_start = threading.Lock()
        self.lock_start.acquire()
        
        """self.lock_pause , allow the user to put a cycle in pause mode, do not access it directly but trought get_pause function"""
        self._lock_pause = threading.Lock()
        self._in_pause = [threading.Lock(), False]
        
        """stop the cycle, False : not stopped"""
        self._stop = [threading.Lock(), True]
        

        
        if self.fake : 
            self.fake_clock = fake_clock(0.01*(2/3))
            self.current_time = self.fake_clock.time()/3600
            self.old_time = self.fake_clock.time()/3600       
        else :
            self.current_time = time.time()/3600
            self.old_time = time.time()/3600

        
        
    def run (self):
        
        print("debut BRBU")
        
        while True :  
            print("Cycle BRBU is waiting for a start order")
            """wait for order to start"""
            self.lock_start.acquire()
            print("Cycle BRBU is starting")
            
            """set all the BR_BU_redy, BU_empty to false """
            for item in self.BR_BU_ready : 
                self.BR_BU_ready[item] = False 
            for item in self.BU_empty : 
                self.BU_empty[item] = False
                
            if self.fake :
                self.current_time = self.fake_clock.time()/3600
                self.old_time = self.fake_clock.time()/3600
            else :
                self.current_time = time.time()/3600
                self.old_time = time.time()/3600
            
            
            
            
            while not self._get_stop() :
                
                """way of knowing time betweeen two round"""
                if self.fake :
                    self.current_time = self.fake_clock.time()/3600
                else :
                    self.current_time = time.time()/3600
                  
               
                """ time betweeen two round in hour"""
                time_laps_hour = (self.current_time - self.old_time) % 216 
                
                """ time betweeen two round in minute"""
                time_laps_minute = (60 * time_laps_hour)%60        
                
                time_laps_second = ((60 * time_laps_minute)/30)%216
                
                print("time"+ str(time_laps_hour))
                #if time_laps_second < 72 :
                if time_laps_hour < 72 : 
                    self.current_state.set_BRBU_state("BU1", "WAIT")
                    self.current_state.set_BRBU_state("BU2", "USE")
                    self.current_state.set_BRBU_state("BU3", "EMPTY")
                    
                    self.BR_BU_ready["BU2"] = False
                    self.BU_empty["BU1"] = False
        
    
    
                    """Day 3 -Day  6  """
                #elif time_laps_second < 144 :
                elif time_laps_hour < 144 :
                    self.current_state.set_BRBU_state("BU1", "USE")
                    self.current_state.set_BRBU_state("BU2", "EMPTY")
                    self.current_state.set_BRBU_state("BU3", "WAIT")
                    
                    self.BR_BU_ready["BU1"] = False
                    self.BU_empty["BU3"] = False
    
            
                    """Day 6 -Day  9  """
                #elif time_laps_second < 216 :
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
                        
                        """check if it is not in pause, not in stop and if volume occupied ... """
                        """name of the pump associatedto this action"""
                        name = "P_BR1_BU1"
                        while self.current_state.get_occupied_volume("BU1") < 0.66 and not self._get_stop() :
                            self.current_state.set_state_pump(name, True)
                            self.get_pause(name,0)
                            time.sleep(0.2)
                            """maybe add : if pump is in manuel-mode, end the manuel mode"""
                        self.current_state.set_state_pump(name, False)
                        
                        
                        
                        
                        """fill BU : full with M2 """
                        name = "P_M2_BU1"
                        while self.current_state.get_occupied_volume("BU1") < 0.90  and not self._get_stop(): 
                            self.current_state.set_state_pump(name, True)
                            self.get_pause(name,0)
                            time.sleep(0.2)
                            """maybe add : if pump is in manuel-mode, end the manuel mode"""
                        self.current_state.set_state_pump(name, False)
        
                        
                        """fill BR : full with M1 """
                        name = "P_M1_BR1"
                        while self.current_state.get_occupied_volume("BR1") < 0.90 and not self._get_stop() : 
                            self.current_state.set_state_pump(name, True)
                            self.get_pause(name,0)
                            time.sleep(0.2)
                            """maybe add : if pump is in manuel-mode, end the manuel mode"""
                        self.current_state.set_state_pump(name, False )
                         
                        
                        """BR1_BU1_ready ready """
                        self.BR_BU_ready["BU1"] = True;                
                        

                
                """if B2 is in WAIT"""
                if self.current_state.get_BRBU_state("BU2") == "WAIT":
                    if not self.BR_BU_ready["BU2"] :
                        
                        """empty BR and fill BU : 2/3 BR -> BU """
                        
                        name = "P_BR2_BU2"
                        while self.current_state.get_occupied_volume("BU2") < 0.66 and not self._get_stop()  :
                            self.current_state.set_state_pump(name, True)
                            self.get_pause(name,0)
                            time.sleep(0.2)
                            """maybe add : if pump is in manuel-mode, end the manuel mode"""
                        self.current_state.set_state_pump(name, False )
                        
                    
                        
                        """fill BU : full with M2 """
                        name = "P_M2_BU2"
                        while self.current_state.get_occupied_volume("BU2") <  0.90 and not self._get_stop() :
                            self.current_state.set_state_pump(name, True)
                            self.get_pause(name,0)
                            time.sleep(0.2)
                            """maybe add : if pump is in manuel-mode, end the manuel mode"""
                        self.current_state.set_state_pump(name, False )
               
                        
                        """fill BR : full with M1 """
                        name = "P_M1_BR2"
                        while self.current_state.get_occupied_volume("BR2") < 0.90 and not self._get_stop()  :
                            self.current_state.set_state_pump(name, True)
                            self.get_pause(name,0)
                            time.sleep(0.2)
                            """maybe add : if pump is in manuel-mode, end the manuel mode"""
                        self.current_state.set_state_pump(name, False )  
                        
                        
                        """BR2_BU2_ready ready """
                        self.BR_BU_ready["BU2"] = True            
                
                """if B3 is in WAIT"""
                if self.current_state.get_BRBU_state("BU3") == "WAIT" :
                    
                    if not self.BR_BU_ready["BU2"] :
                        
                        """empty BR and fill BU : 2/3 BR -> BU """
                        name = "P_BR3_BU3"
                        while self.current_state.get_occupied_volume("BU3") < 0.66 and not self._get_stop() :
                            self.current_state.set_state_pump(name, True)
                            self.get_pause(name,0)
                            time.sleep(0.2)
                            """maybe add : if pump is in manuel-mode, end the manuel mode"""
                        self.current_state.set_state_pump(name, False )  
                 
                 
                        """fill BU : full with M2 """
                        name = "P_M2_BU3"
                        while self.current_state.get_occupied_volume("BU3") < 0.90 and not self._get_stop()  :
                            self.current_state.set_state_pump(name, True)
                            self.get_pause(name,0)
                            time.sleep(0.2)
                            """maybe add : if pump is in manuel-mode, end the manuel mode"""
                        self.current_state.set_state_pump(name, False )  
                        
                        
                        """fill BR : full with M1 """
                        name = "P_M1_BR3"
                        while self.current_state.get_occupied_volume("BR3") < 0.90 and not self._get_stop()  :
                            self.current_state.set_state_pump(name, True)
                            self.get_pause(name,0)
                            time.sleep(0.2)
                            """maybe add : if pump is in manuel-mode, end the manuel mode"""
                        self.current_state.set_state_pump(name, False )    
                        
                        
                        """BR_BU_ready ready """
                        self.BR_BU_ready["BU3"] = True;
                
                
                if self.current_state.get_BRBU_state("BU1") == "EMPTY":
                    """for testing purposes, emptying BU"""
                    if not self.BU_empty["BU1"]  : 
                        
                        """function to complete, action to do at the begining of EMPTY"""
                        name = "empty_BU1_S"
                        while self.current_state.get_occupied_volume("BU1") > 0.1 and not self._get_stop()  :
                            self.current_state.set_current_action(name, True)
                            self.get_pause(name, 1)
                            time.sleep(0.2)
                        self.current_state.set_current_action(name, False)
                        
                        self.BU_empty["BU1"] = True  
                        
                          
                    
                if self.current_state.get_BRBU_state("BU2") == "EMPTY":
                    if not self.BU_empty["BU2"]  :
                        """function to complete, action to do at the begining of EMPTY"""
                        name = "empty_BU2_S" 
                        while self.current_state.get_occupied_volume("BU2") > 0.1 and not self._get_stop() :
                            self.current_state.set_current_action(name, True)
                            self.get_pause(name, 1)
                            time.sleep(0.2)
                        self.current_state.set_current_action(name, False)
                        self.BU_empty["BU2"] = True 
                         
                            
                    
                if self.current_state.get_BRBU_state("BU3") == "EMPTY":
                    
                    if not self.BU_empty["BU3"]  :
                        """function to complete, action to do at the begining of EMPTY"""
                        name = "empty_BU3_S"
                        while self.current_state.get_occupied_volume("BU3") > 0.1 and not self._get_stop() :
                            self.current_state.set_current_action(name, True)
                            self.get_pause(name, 1)
                            time.sleep(0.2)
                        self.current_state.set_current_action(name, False) 
                        self.BU_empty["BU3"] = True
                        
                    
                
                
                time.sleep(1)
                
                 
            
    
    def reset(self):
        """function to call to rest BU_empty et BRBU_ready, to do the filling at the right time"""
        for item in self.current_state.BRBU_state : 
            if not self.current_state.get_BRBU_state(item) == "WAIT" : 
                self.current_state.set_BRBU_state(item, False)
                
            if not self.current_state.get_BRBU_state(item) == "EMPTY" : 
                self.BU_empty[item] = False
    
    """return the value of self.stop"""
    def _get_stop(self):

        self._stop[0].acquire()
        state = self._stop[1]
        self._stop[0].release()
        return state
    
    """set stop to state, will interrupt the cycle definitly if False, """
    def _set_stop(self, state):
            
        self._stop[0].acquire()
        self._stop[1] = state 
        self._stop[0].release()
        
    
    def start_stop_cycle(self):
        """if not in pause, just stop the programme"""
        if not self._get_in_pause() : 
            if not self._get_stop() : 
                self._set_stop(True)  
            else : 
                """set self.stop to False, in order to pursue """
                self._set_stop(False)
                self.lock_start.release()
        else : 
            print("BRBU in pause mode : no stop possible because in pause mode, unpaused it to  be able to stop it after")

    """
    def set_stop_start(self, state):
    
        if not state == self._get_stop() : 
            if state : 
                
            
            else : 
    """
        
        
    def _set_in_pause(self, state):
        self._in_pause[0].acquire()
        self._in_pause[1] = state
        self._in_pause[0].release()
        
    
    def _get_in_pause(self): 
        self._in_pause[0].acquire()
        state = self._in_pause[1]
        self._in_pause[0].release()
        return state
        

         
        
    """get in or get out of the pause mode"""
    def pause(self):
        
        """pause is possible only if if is not already stopped"""
        if not self._get_stop() : 
            """if already in pause """
            if self._get_in_pause() : 
                """get out from pause mode"""
                self._lock_pause.release()
                self._set_in_pause(False)
                
                """if not in pause mode"""
            else : 
                """get in the mode pause"""
                self._lock_pause.acquire()
                self._set_in_pause(True)
        
        else : 
            print("BRBU in stop mode : no pause possible because it is not running")
            
        
        
    """stop the programme if someone took the lock, until someone release the lock"""
    def get_pause(self, name, type):
        """name : name of the action running, type : type of the action running )  """
        
        """if in pause"""
        if self._get_in_pause() :  
            """turn off the action"""
            
            """if it is a pump"""
            if type == 0 : 
                self.current_state.set_state_pump(name, False)
                
                
                """will block the thread if in pause mode"""
                self._lock_pause.acquire()
                self._lock_pause.release()
                
                """turn on the pump"""
                self.current_state.set_state_pump(name, True)
                
                """if it is an action"""
            elif type == 1 :
                self.current_state.set_current_action(name, False)
                
                
                """will block the thread if in pause mode"""
                self._lock_pause.acquire()
                self._lock_pause.release()
                
                """turn on the pump"""
                self.current_state.set_current_action(name, True) 
                 
        return True
    
    
    """action to set the system in the right situation to start the production-cycle"""
    def initialization(self):
        """initial situation : BR1 = 1 , BR2 = 2/3 , BR3 = 1/3"""
        
        """filling BR2 with M1"""
        name = "P_M1_BR2"
        while self.current_state.get_occupied_volume("BR2") < 0.9  :
            self.current_state.set_current_action(name, True)
            time.sleep(0.2)
        self.current_state.set_current_action(name, False) 
        
        """filling BR3 with M1"""
        name = "P_M1_BR3"
        while self.current_state.get_occupied_volume("BR3") < 0.9  :
            self.current_state.set_current_action(name, True)
            time.sleep(0.2)
            
        print ("Initialisation finished : production cycle can be launched")
        self.current_state.set_current_action(name, False) 
         

        
             

   
