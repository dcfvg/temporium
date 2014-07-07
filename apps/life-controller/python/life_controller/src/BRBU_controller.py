'''
Created on Apr 29, 2014

@author: glogzy (tete de thon)
'''
import time
from time import localtime, strftime
from com_arduino import*
from current_state import*
from fake_clock import *
from action_thread.thread_BRBU_controller_unpaused import*

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
 
  
        
        """if wish to have a fake time"""
        self.fake = False
        
        """self.lock to wait for start, release it in order to start"""
        self.lock_start = threading.Lock()
        self.lock_start.acquire()
        
        """self.lock_pause , allow the user to put a cycle in pause mode, do not access it directly but trought _get_pause function"""
        self._lock_pause = threading.Lock()
        self._in_pause = [threading.Lock(), False]
        
        """stop the cycle, False : not stopped"""
        self._stop = [threading.Lock(), True]
        
        """values of configuration for production cycle : ex level to fill .. etc"""
        self._BRBU_controller_value = {"BR_FULL" :[threading.Lock(), 0],\
                                       "BU_FULL" :[threading.Lock(), 0],\
                                       "BU_EMPTY" :[threading.Lock(), 0],\
                                       "FILLING_BR_BU" :[threading.Lock(), 0],\
                                       }
        
        self._reset_time()

        
        
    def run (self):
        
        print("debut BRBU")
        
        
        self.set_old_current_state()
        
        #print ("daz : " + str(self.current_time_cycle))
        
        while True :  
            print("Cycle BRBU is waiting for a start order")
            
            """wait for order to start"""
            self.lock_start.acquire()
            print("Cycle BRBU is starting")
            
            """read the config value, in config manager"""
            self._load_value_config()
            
            while self.current_state.get_BRBU_controller_state("run") :
                
                """way of knowing time betweeen two round"""
                if self.fake :
                    self.current_time_cycle = self.current_time_cycle + (self.fake_clock.time() - self.old_time)
                    self.old_time = self.fake_clock.time().time()
                else :
                    self.current_time_cycle = self.current_time_cycle + (time.time() - self.old_time)
                    self.old_time = time.time()
                  
               
                """ time betweeen two round in hour"""
                time_laps_hour = self.current_time_cycle /3600
                
                """ time betweeen two round in minute"""
                time_laps_minute = (60 * time_laps_hour)%60        
                
                time_laps_second = (60 * time_laps_minute)%60
                
                self.save_current_situation(True)
                #if time_laps_second < 72 :
                if time_laps_hour < 72 : 
                    self.current_state.set_BU_state("BU1", "WAIT")
                    self.current_state.set_BU_state("BU2", "USE")
                    self.current_state.set_BU_state("BU3", "EMPTY")
                    
                    self.BR_BU_ready["BU2"] = False
                    self.BU_empty["BU1"] = False
        
    
    
                    """Day 3 -Day  6  """
                #elif time_laps_second < 144 :
                elif time_laps_hour < 144 :
                    self.current_state.set_BU_state("BU1", "USE")
                    self.current_state.set_BU_state("BU2", "EMPTY")
                    self.current_state.set_BU_state("BU3", "WAIT")
                    
                    self.BR_BU_ready["BU1"] = False
                    self.BU_empty["BU3"] = False
    
            
                    """Day 6 -Day  9  """
                #elif time_laps_second < 216 :
                elif time_laps_hour < 216 :
                    self.current_state.set_BU_state("BU1", "EMPTY")
                    self.current_state.set_BU_state("BU2", "WAIT")
                    self.current_state.set_BU_state("BU3", "USE")
                    
                    self.BR_BU_ready["BU3"] = False
                    self.BU_empty["BU2"] = False
                
                
                #for item in self.current_state.BRBU_state : 
                #  print (item + " " + str(self.current_state.get_BU_state(item)) )
    
                """Action on BU - BR to produce alguae"""
                
                """if B1 is in WAIT"""
                if self.current_state.get_BU_state("BU1") == "WAIT":
                    
                    """At the begining of WAIT for C1"""
                    if not self.BR_BU_ready["BU1"] :
                        
                        """empty BR and fill BU : 2/3 BR -> BU """
                        
                        """check if it is not in pause, not in stop and if volume occupied ... """
                        """name of the pump associatedto this action"""
                        
                        """empty BR and fill BU : 2/3 BR -> BU """
                        
                        self.fill_BRBU("P_BR1_BU1", "BU1",self.get_BRBU_controller("FILLING_BR_BU") )
                        """saving the state"""
                        self.save_current_situation(True)
                        
                        """fill BU : full with M2 """
                        self.fill_BRBU("P_M2_BU1", "BU1", self.get_BRBU_controller("BU_FULL"))
                        """saving the state"""
                        self.save_current_situation(True)
        
                        
                        """fill BR : full with M1 """
                        self.fill_BRBU("P_M1_BR1", "BR1",  self.get_BRBU_controller("BR_FULL"))
                        """saving the state"""
                        self.save_current_situation(True)
        

                        """BR1_BU1_ready ready """
                        self.BR_BU_ready["BU1"] = True;
                        """saving the state"""
                        self.save_current_situation(True)               
                        

                
                """if B2 is in WAIT"""
                if self.current_state.get_BU_state("BU2") == "WAIT":
                    if not self.BR_BU_ready["BU2"] :
                        
                        """empty BR and fill BU : 2/3 BR -> BU """
                        self.fill_BRBU("P_BR2_BU2", "BU2", self.get_BRBU_controller("FILLING_BR_BU") )
                        """saving the state"""
                        self.save_current_situation(True)
                        
                        """fill BU : full with M2 """
                        self.fill_BRBU("P_M2_BU2", "BU2", self.get_BRBU_controller("BU_FULL"))
                        """saving the state"""
                        self.save_current_situation(True)
                        
                        """fill BR : full with M1 """
                        self.fill_BRBU("P_M1_BR2", "BR2", self.get_BRBU_controller("BR_FULL"))
                        """saving the state"""
                        self.save_current_situation(True)  
                    
                        """BR2_BU2_ready ready """
                        self.BR_BU_ready["BU2"] = True
                        """saving the state"""
                        self.save_current_situation(True)            
                
                """if B3 is in WAIT"""
                if self.current_state.get_BU_state("BU3") == "WAIT" :
                    
                    if not self.BR_BU_ready["BU2"] :
                        
                        """empty BR and fill BU : 2/3 BR -> BU """
                        self.fill_BRBU("P_BR3_BU3", "BU3", self.get_BRBU_controller("FILLING_BR_BU") )
                        """saving the state"""
                        self.save_current_situation(True)
                        
                        """fill BU : full with M2 """
                        self.fill_BRBU("P_M2_BU3", "BU3", self.get_BRBU_controller("BU_FULL") )
                        """saving the state"""
                        self.save_current_situation(True)
                          
                        """fill BR : full with M1 """
                        self.fill_BRBU("P_M1_BR3", "BR3", self.get_BRBU_controller("BR_FULL"))
                        """saving the state"""
                        self.save_current_situation(True)
                        
                        
                        """BR_BU_ready ready """
                        self.BR_BU_ready["BU3"] = True;
                        """saving the state"""
                        self.save_current_situation(True)
                
                
                if self.current_state.get_BU_state("BU1") == "EMPTY":
                    """for testing purposes, emptying BU"""
                    if not self.BU_empty["BU1"]  : 
                        
                        """function to complete, action to do at the begining of EMPTY"""
                        self.empty_BU("empty_BU1_S", "BU1", self.get_BRBU_controller("BU_EMPTY"))
                        """saving the state"""
                        self.save_current_situation(True)
                        
                          
                    
                if self.current_state.get_BU_state("BU2") == "EMPTY":
                    if not self.BU_empty["BU2"]  :
                        """function to complete, action to do at the begining of EMPTY"""
                        self.empty_BU("empty_BU2_S", "BU2", self.get_BRBU_controller("BU_EMPTY"))
                        """saving the state"""
                        self.save_current_situation(True)
                              
                    
                if self.current_state.get_BU_state("BU3") == "EMPTY":
                    
                    if not self.BU_empty["BU3"]  :
                        """function to complete, action to do at the begining of EMPTY"""
                        self.empty_BU("empty_BU3_S", "BU3", self.get_BRBU_controller("BU_EMPTY"))
                        """saving the state"""
                        self.save_current_situation(True)
                time.sleep(1)
                
            """when stopped, save current_situation autostart to False"""
            self.save_current_situation(False)

                        
    """ACTION TAKEN BY BRBU_CONTROLLER"""          
    """fill container_name, with pump_name unti volume_order in conatainer_name"""
    def fill_BRBU(self, pump_name, container_name, volume_order):
            
            while self.current_state.get_occupied_volume(container_name) < volume_order and self.current_state.get_BRBU_controller_state("run") :
                self.current_state.set_information_asked("level", True)
                if not self.current_state.get_information_asked("level") : 
                    print ("no information about level : BR_BU cycle in pause")
                    self.current_state.set_BRBU_controller_state("pause", True)
                    self.try_to_unpaused()
                self.current_state.set_state_pump(pump_name, True)
                self._get_pause(pump_name,0)
                time.sleep(0.2)
                """maybe add : if pump is in manuel-mode, end the manuel mode"""
            self.current_state.set_state_pump(pump_name, False)
            
            self.current_state.set_information_asked("level", False)
        
    
    """empty container_name with action_name until volume_order in container_name"""   
    def empty_BU(self, action_name, container_name, volume_order):

        
        """to avoid wasting BU"""
        if False : 
            self.current_state.set_information_asked("level", True)
            while self.current_state.get_occupied_volume(container_name) > volume_order and self.current_state.get_BRBU_controller_state("run")  :
                self.current_state.set_information_asked("level", True)
                if not self.current_state.get_information_asked("level") : 
                    print ("no information about level : BR_BU cycle in pause")
                    self.current_state.set_BRBU_controller_state("pause", True)
                    self.try_to_unpaused()
                self.current_state.set_current_action(action_name, True)
                self._get_pause(action_name, 1)
                time.sleep(0.2)
            self.current_state.set_current_action(action_name, False)
        
            self.current_state.set_information_asked("level", False)
        self.BU_empty[container_name] = True 
    
    

    def reset(self):
        """function to call to reset BU_empty et BRBU_ready, to do the filling at the right time"""
        for item in self.current_state.BRBU_state : 
            if not self.current_state.get_BU_state(item) == "WAIT" : 
                self.current_state.set_BU_state(item, "NULL")
                
            if not self.current_state.get_BU_state(item) == "EMPTY" : 
                self.BU_empty[item] = False
    
    """CYCLE MANAGEMENT"""
        
    
    def try_to_unpaused(self):
        self.thread_BRBU_controller_unpaused = thread_BRBU_controller_unpaused(self.current_state)
        self.thread_BRBU_controller_unpaused.start()
    """reset cycle's time"""
    def _reset_time(self):
        if self.fake :
            self.current_time_cycle = 0
            self.old_time = self.fake_clock.time()
        else :
            self.current_time_cycle = 0
            self.old_time = time.time()
        
        """set all the BR_BU_redy, BU_empty to false """
        for item in self.BR_BU_ready : 
            self.BR_BU_ready[item] = False 
        for item in self.BU_empty : 
            self.BU_empty[item] = False
    
    
     
    """stop the programme if someone took the lock, until someone release the lock"""
    def _get_pause(self, name, type):
        """name : name of the action running, type : type of the action running )  """
        
        """if in pause"""
        if self.current_state.get_BRBU_controller_state("pause"): 
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
    
    
    
    """INITIALISATION"""
    """action to set the system in the right situation to start the production-cycle"""
    def initialization(self):
        """initial situation : BR1 = 1 , BR2 = 2/3 , BR3 = 1/3"""
        """fill up BR with M1"""
        
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
    
    """SAVING/READING OLD SITUATION"""
    def set_old_current_state(self):
        print("read old situation")
        file = open("save_current_situation/BRBU_current_state.txt", "r")
        
        auto_start = False
        
        for ligne in file :
            
            """Take out the end symbols (\n)"""
            ligne = ligne.strip()
            """split on  ':' """
            list = ligne.split(":")
        
            """if auto_start is yes, then set auto_start to True"""
            if list[0].strip() == "auto_start" :
                auto_start = (list[1].strip() == "True" )
        print ("BRBU_controller auto_start : "  + str(auto_start))
        file.close()
        
        file = open("save_current_situation/BRBU_current_state.txt", "r")
        if auto_start :
             
            for ligne in file :
                """Take out the end symbols (\n)"""
                ligne = ligne.strip()
                """split on  ':' """
                list = ligne.split(":")    
                if list[0].strip() == "BU1" :
                    if list[1].strip() == "READY" :
                        self.BR_BU_ready["BU1"] = ( list[2].strip() == "True")
                    elif list[1].strip() == "EMPTY" :
                        self.BU_empty["BU1"] = ( list[2].strip() == "True")
                        
                elif list[0].strip() == "BU2" :
                    if list[1].strip() == "READY" :
                        self.BR_BU_ready["BU2"] = ( list[2].strip() == "True")
                    elif list[1].strip() == "EMPTY" :
                        self.BU_empty["BU2"] = ( list[2].strip() == "True")
                
                elif list[0].strip() == "BU3" :
                    if list[1].strip() == "READY" :
                        self.BR_BU_ready["BU3"] = ( list[2].strip() == "True")
                    elif list[1].strip() == "EMPTY" :
                        self.BU_empty["BU3"] = ( list[2].strip() == "True")
                
                elif list[0].strip() == "time_cycle_second" :
                    self.current_time_cycle = int(list[1].strip())
            
            
            """start the cycle with the situation form the saved file"""
            
            """first get out from pause"""
            self.current_state.set_BRBU_controller_state("pause", False) 
            
            self.current_state.set_BRBU_controller_state("run", True) 
            """set self.stop to False, in order to pursue """
            #self._set_stop(False)
            #self.lock_start.release()
            """set BRBU_controller_state to True in self.current_state"""
            #self.current_state._set_BRBU_controller_state(True)
              
        
    def save_current_situation(self, auto_start_state):
        #print("saving BRBU_controller " + str(auto_start_state))
        """stock the current time of the cyle"""
        if self.fake : 
            current_time_cycle_save = int((self.current_time_cycle + (self.fake_clock.time() - self.old_time)))
        else : 
            current_time_cycle_save = int((self.current_time_cycle + (time.time() - self.old_time)))
        """ time betweeen two round in hour"""
        time_laps_hour = current_time_cycle_save /3600
        """ time betweeen two round in minute"""
        time_laps_minute = (60 * time_laps_hour)%60        
        time_laps_second = (60 * time_laps_minute)%60
        
        """a tester de ne l'ouvrir qu'au depart"""
        save_file = open("save_current_situation/BRBU_current_state.txt", "w")
        save_file.write("Temporium : BRBU_controller "+ " \n")
        save_file.write("auto_start : "+ str(auto_start_state) + " \n")
        save_file.write("time_save_second : "+ str(int(time.time())) + " \n")
        save_file.write("time_save_second : "+ time.strftime("%a, %d %b %Y %H:%M:%S +0000",time. localtime()) + "\n")
        save_file.write("time_cycle_second : "+ str(int(current_time_cycle_save)) + " \n")
        save_file.write("time_cycle : "+ str(int(time_laps_hour))+ "h" + str(int(time_laps_minute)) + "m" + str(int(time_laps_second)) + " \n")
        save_file.write("BU1 : READY : " + str(self.BR_BU_ready["BU1"])+ " \n")
        save_file.write("BU2 : READY : " + str(self.BR_BU_ready["BU2"])+ " \n")
        save_file.write("BU3 : READY : " + str(self.BR_BU_ready["BU3"])+ " \n")
        save_file.write("BU1 : EMPTY : " + str(self.BU_empty["BU1"])+ " \n")
        save_file.write("BU2 : EMPTY : " + str(self.BU_empty["BU2"])+ " \n")
        save_file.write("BU3 : EMPTY : " + str(self.BU_empty["BU3"]))
        save_file.flush()
         

    """LOADING CONFIGURTION VALUES"""
    """loading values from config_manager"""
    def _load_value_config(self):
        for item in self._BRBU_controller_value :
            value =  self.current_state.config_manager.get_BRBU_controller(item)
            self._set_BRBU_controller(item, value)
    
    def _set_BRBU_controller(self, name, value):
        self._BRBU_controller_value[name][0].acquire()
        self._BRBU_controller_value[name][1] = value      
        self._BRBU_controller_value[name][0].release()
    
    """return the value corresponding to the name you asked : ex "BU_FULL" here""" 
    def get_BRBU_controller(self, name):
        self._BRBU_controller_value[name][0].acquire()
        value = self._BRBU_controller_value[name][1]       
        self._BRBU_controller_value[name][0].release()
        return value
             

   
