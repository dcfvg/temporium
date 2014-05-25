'''
Created on Apr 27, 2014

@author: Cactus
'''

import threading
import time
from action_thread.AQ_filtration import *
from action_thread.fill_BU_AQ import *
from action_thread.auto_AQ_filtration import *
from action_thread.renew_light_AQ_BU import *
from action_thread.empty_BU_S import *

class current_state(object):
    """ Gather all the informations about the state of the installation"""
    
    def __init__(self,un_com_arduino  ):
        
        self.com_arduino = un_com_arduino
        
        """state of each pump : { P_M1_BR1 : [Lock,True] , P_M1_BR2 : [Lock, False] , ...} """
        #self.state_pumps = dict()
        self._state_pumps = { "P_M1_BR1" : [threading.Lock(),False] , "P_M1_BR2" : [threading.Lock(),False], "P_M1_BR3" : [threading.Lock(),False],\
                             "P_BR1_BU1" : [threading.Lock(),False], "P_BR2_BU2" : [threading.Lock(),False] , "P_BR3_BU3" : [threading.Lock(),False],\
                             "P_M2_BU1" : [threading.Lock(),False], "P_M2_BU2" : [threading.Lock(),False] , "P_M2_BU3" : [threading.Lock(),False], "P_M2_AQ" : [threading.Lock(),False],\
                             "P_BU1_FI" : [threading.Lock(),False], "P_BU2_FI" : [threading.Lock(),False] , "P_BU3_FI" : [threading.Lock(),False],\
                             "P_AQ_S" : [threading.Lock(),False], "P_AQ_FI" : [threading.Lock(),False] , "P_FI_AQ_1" : [threading.Lock(),False], "P_FI_AQ_3" : [threading.Lock(),False],\
                             "P_FI_S" : [threading.Lock(),False] }
        
        """state of the EL {"AQ" : {"HIGH" : [threading.Lock(),False,1], "MEDIUM" : [threading.Lock(),False,0.66] },... }"""
        self._state_EL = dict()
        
        
        """Occupied volume for each container : { M1 : [Lock, 0.75] , M2 : ...} """
        self._occupied_volume = dict()
        
        """time of each cycle : { C1 : [Lock, 75] , C2 : ...}"""
        self.time_cycle = dict()
        
        """Number of usage for each BU : { BU1 : 0 , BU2 : 23, ...} """
        self.number_usage = dict()
        
        """BRBU_controller state"""
        self._BRBU_state = {"BU1" : [threading.Lock(), "USE"],"BU2" : [threading.Lock(), "WAIT"],"BU3" : [threading.Lock(), "EMPTY"] }
        
        """current_action"""
        self._current_action = {"AQ_filtration" : [threading.Lock(),False],\
                                "fill_BU1_AQ" : [threading.Lock(),False],\
                                "fill_BU2_AQ" : [threading.Lock(),False] ,\
                                "fill_BU3_AQ" : [threading.Lock(),False],\
                                "empty_BU1_S" : [threading.Lock(),False],\
                                "empty_BU2_S" : [threading.Lock(),False],\
                                "empty_BU3_S" : [threading.Lock(),False],\
                                 }
        
        """current_action_evolved"""
        self._current_action_evolved = {"auto_AQ_filtration" : [threading.Lock(),False],\
                                        "renew_light_AQ_BU1" : [threading.Lock(),False],\
                                        "renew_light_AQ_BU2" : [threading.Lock(),False],\
                                        "renew_light_AQ_BU3" : [threading.Lock(),False],\
                                 }
        
        """AQ_concentration"""
        self._concentration = {"AQ" :[threading.Lock(), 0]}
        
        self.last_time = time.time()
        
        self._formation_rate = [threading.Lock(), 35]
        
        """if there is a GUI or not"""
        self.GUI = False 
        
        "emergency stop "  
        self._keep_going = [threading.Lock(), True]
        
        """initialize all values after a log_start.txt"""
        self.__setState__()
        #self._check_all_EL()
    
        #self.client_connected = 
    
    def P_BR1_BU1(self, state):
        name= 'P_BR1_BU1'
        self.set_state_pump( name, state )
        
    def P_BR2_BU2(self, state):
        name= 'P_BR2_BU2'
        self.set_state_pump( name, state )
    
    def P_BR3_BU3(self, state):
        name = 'P_BR3_BU3'
        self.set_state_pump( name, state )
           
    def P_BU1_FI(self, state):
        name = 'P_BU1_FI'
        self.set_state_pump( name, state )
                
    def P_BU2_FI(self, state):
        name = 'P_BU2_FI'
        self.set_state_pump( name, state )
    
    def P_BU3_FI(self, state):
        name = 'P_BU3_FI'
        self.set_state_pump( name, state )
                
    def P_M1_BR1(self, state):
        name = 'P_M1_BR1'
        self.set_state_pump( name, state )
   
    def P_M1_BR2(self, state):
        name = 'P_M1_BR2'
        self.set_state_pump( name, state )
                
    def P_M1_BR3(self, state):
        name = 'P_M1_BR3'
        self.set_state_pump( name, state )
                
    def P_M2_BU1(self, state):
        name = 'P_M2_BU1'
        self.set_state_pump( name, state )
   
    def P_M2_BU2(self, state):
        name = 'P_M2_BU2'
        self.set_state_pump( name, state )
        
    def P_M2_BU3(self, state):
        name = 'P_M2_BU3'
        self.set_state_pump( name, state )
                           
    def P_M2_AQ(self, state):
        name = 'P_M2_AQ'
        self.set_state_pump( name, state )
    
    def P_AQ_S(self, state):
        name = 'P_AQ_S'
        self.set_state_pump( name, state )
        
    def P_AQ_FI(self, state):
        name = 'P_AQ_FI'
        self.set_state_pump( name, state )
        
    def P_FI_AQ_1(self, state):
        name = 'P_FI_AQ_1'
        self.set_state_pump( name, state )
        
    def P_FI_AQ_3(self, state):
        name = 'P_FI_AQ_3'
        self.set_state_pump( name, state )
    
    def P_FI_S(self, state):
        name = 'P_FI_S'
        self.set_state_pump( name, state )
          
    def AQ_filtration(self, state):
        """to filter the aquarium"""
        name = "AQ_filtration"
        self.set_current_action(name, state)
    
    def fill_BU1_AQ(self,state):
        """to fill AQ with BU1"""
        name = "fill_BU1_AQ"
        self.set_current_action(name, state)
    
    def fill_BU2_AQ(self, state):
        """to fill AQ with BU2"""
        name = "fill_BU2_AQ"
        self.set_current_action(name, state)
        
    def fill_BU3_AQ(self, state):
        """to fill AQ with BU3"""
        name = "fill_BU3_AQ"
        self.set_current_action(name, state)
        
    def fill_BU_AQ(self, BU_name, state):
        """to fill AQ with BU_name"""
        action_name = "fill_"+BU_name+"_AQ"
        self.set_current_action(action_name, state)
    
    def empty_BU1_S(self,state):
        """to fill AQ with BU1"""
        name = "empty_BU1_S"
        self.set_current_action(name, state)
    
    def empty_BU2_S(self, state):
        """to fill AQ with BU2"""
        name = "empty_BU2_S"
        self.set_current_action(name, state)
        
    def empty_BU3_S(self, state):
        """to fill AQ with BU3"""
        name = "empty_BU3_S"
        self.set_current_action(name, state)
        
        
    """Order to liftDown and liftUp, screenDown and screenUp"""
    def liftDown(self):
        print("LiftDown")

    def liftUp(self):
        print("liftUp")

    def screenDown(self):
        print("screenDown")

    def screenUp(self):
        print("screenUp")
    
    
    """do not use this function"""       
    def _set_current_action(self, name, state):
        self._current_action[name][0].acquire()
        self._current_action[name][1] = state
        self._current_action[name][0].release()
        
    def set_current_action(self, name, state):
        """check if there is no action running"""
        b = True
        for item in self._current_action : 
            if not item == name :  
                if self.get_current_action(item) : 
                    b = False
        
        """if there is no action running"""
        if b :
            if not self.get_current_action(name) == state : 
                if name == "AQ_filtration" : 
                    if state : 
                        """start the thread to for a filtration, only if there is no filtration at the same time"""
                        if not self.get_current_action("AQ_filtration") :
                            action = AQ_filtration(self)
                            action.start()
                    else : 
                        """set the action to end, and will stop the current action""" 
                        self._set_current_action("AQ_filtration",False)
                        
                elif name == "fill_BU1_AQ" : 
                    if state : 
                        """start the thread to for a filtration, only if there is no filtration at the same time"""
                        if not self.get_current_action("fill_BU1_AQ") :
                            action = fill_BU_AQ(self,"BU1")
                            action.start()
                        
                    else : 
                        self._set_current_action("fill_BU1_AQ",False)
                elif name == "fill_BU2_AQ" : 
                    if state : 
                        """start the thread to for a filtration, only if there is no filtration at the same time"""
                        if not self.get_current_action("fill_BU2_AQ") :
                            action = fill_BU_AQ(self,"BU2")
                            action.start()
                        
                    else : 
                        self._set_current_action("fill_BU2_AQ",False)
                elif name == "fill_BU3_AQ" :
                    if state : 
                        """start the thread to for a filtration, only if there is no filtration at the same time"""
                        if not self.get_current_action("fill_BU3_AQ") :
                            action = fill_BU_AQ(self,"BU3")
                            action.start()
                    else : 
                        self._set_current_action("fill_BU3_AQ",False)
                
                elif name == "empty_BU1_S" :
                    if state : 
                        """start the thread for a emptying, only if there is no filtration at the same time"""
                        if not self.get_current_action("empty_BU1_S") :
                            action = empty_BU_S(self,"BU1")
                            action.start()
                    else : 
                        self._set_current_action("empty_BU1_S",False)
                
                elif name == "empty_BU2_S" :
                    if state : 
                        """start the thread to for a filtration, only if there is no filtration at the same time"""
                        if not self.get_current_action("empty_BU2_S") :
                            action = empty_BU_S(self,"BU2")
                            action.start()
                    else : 
                        self._set_current_action("empty_BU2_S",False)
                
                elif name == "empty_BU3_S" :
                    if state : 
                        """start the thread to for a filtration, only if there is no filtration at the same time"""
                        if not self.get_current_action("empty_BU3_S") :
                            action = empty_BU_S(self,"BU3")
                            action.start()
                    else : 
                        self._set_current_action("empty_BU3_S",False)
        else : 
            print(name + " to "+ str(state) + " impossible : already a task running")                
        
    
    """do not use this function"""       
    def _set_current_action_evolved(self, name, state):
        self._current_action_evolved[name][0].acquire()
        self._current_action_evolved[name][1] = state
        self._current_action_evolved[name][0].release()
    
    def get_current_action_evolved(self, name):
        self._current_action_evolved[name][0].acquire()
        state = self._current_action_evolved[name][1]
        self._current_action_evolved[name][0].release()
        return state
    
    def set_current_action_evolved(self, name, state):
        """check if there is no action running"""
        b = True
        for item in self._current_action_evolved : 
            if not item == name :
                if self.get_current_action_evolved(item) : 
                    b = False
        """if there is no action running"""
        if b : 
            if not self.get_current_action_evolved(name) == state : 
                if name == "auto_AQ_filtration" : 
                    if state : 
                        """start the thread to for a filtration, only if there is no filtration at the same time"""
                        if not self.get_current_action_evolved("auto_AQ_filtration") :
                            action = auto_AQ_filtration(self)
                            action.start()
                    else : 
                        """set the action to end, and will stop the current action""" 
                        self._set_current_action_evolved("auto_AQ_filtration",False)
                if name == "renew_light_AQ_BU1" : 
                    if state : 
                        """start the thread to for a filtration, only if there is no filtration at the same time"""
                        if not self.get_current_action_evolved("renew_light_AQ_BU1") :
                            action = renew_light_AQ_BU(self,"BU1")
                            action.start()
                    else : 
                        """set the action to end, and will stop the current action""" 
                        self._set_current_action_evolved("renew_light_AQ_BU1",False)
                if name == "renew_light_AQ_BU2" : 
                    if state : 
                        """start the thread to for a filtration, only if there is no filtration at the same time"""
                        if not self.get_current_action_evolved("renew_light_AQ_BU2") :
                            action = renew_light_AQ_BU(self,"BU2")
                            action.start()
                    else : 
                        """set the action to end, and will stop the current action""" 
                        self._set_current_action_evolved("renew_light_AQ_BU2",False)
                if name == "renew_light_AQ_BU3" : 
                    if state : 
                        """start the thread to for a filtration, only if there is no filtration at the same time"""
                        if not self.get_current_action_evolved("renew_light_AQ_BU3") :
                            action = renew_light_AQ_BU(self,"BU3")
                            action.start()
                    else : 
                        """set the action to end, and will stop the current action""" 
                        self._set_current_action_evolved("renew_light_AQ_BU3",False)
            
        else : 
            print("already a evolved task running")   
        
        
    def get_current_action(self, name):
        self._current_action[name][0].acquire()
        state = self._current_action[name][1]
        self._current_action[name][0].release()
        return state
        

    def get_state_pump(self, name):
        self._state_pumps[name][0].acquire()
        state = self._state_pumps[name][1]
        self._state_pumps[name][0].release()
        return state
    
    """do not use this function from outside"""
    def _set_state_pump(self, name, state ):
        self._state_pumps[name][0].acquire()
        self._state_pumps[name][1] = state
        self._state_pumps[name][0].release()
    """use this function to set a pump state"""
    
    def set_state_pump(self, name, state ):
        """action only if new state is different from current state"""
        if not self.get_state_pump( name) == state:
            """ask com arduino to set the pump"""
            order_ok = self.com_arduino.pump_order(name,state)
            
            """if com_arduino return True, it means order has been successfully conducted""" 
            if order_ok :
                self._set_state_pump(name, state )
            else : 
                print("fail to activate or desactivate " + name )
            
            
            self.refresh_windows()
            #for item in self._occupied_volume : 
                #print(item + " " + str(self.get_occupied_volume(item)))
    
    def get_occupied_volume(self, name):
        self._occupied_volume[name][0].acquire()
        v = self._occupied_volume[name][1]
        self._occupied_volume[name][0].release()
        return v
    
    def set_occupied_volume(self, name, v):
        """no need to have more precision"""
        v = round(v,2)
        self._occupied_volume[name][0].acquire()
        self._occupied_volume[name][1] = v
        self._occupied_volume[name][0].release()
        """refresh GUI"""
        #print("daz" + name + " " + str(v))
        #print (name + " set to " + str(v))
        self.refresh_windows()
  
        
        return bool
      
    def get_concentration(self, container_name):
        """get the AQ_concentration"""
        self._concentration[container_name][0].acquire()
        value = self._concentration[container_name][1]
        self._concentration[container_name][0].release()
        return value
         
    def set_concentration(self,container_name,  value):
        """set the AQ_concentration"""
        self._concentration[container_name][0].acquire()
        self._concentration[container_name][1]= value
        self._concentration[container_name][0].release()
        
        print( "concentration" + container_name + "set to " + str(value) )
        
        
    """do not use this function"""
    def _set_state_EL(self,name_container, name_EL, state):
        """name_container : AQ , name_EL : HIGH"""
        """set the state of the electrode in state_EL, and set the occupied_volume associated to occupied_volume"""
        if not state == self._get_state_EL(name_container, name_EL) : 
            
            self.set_occupied_volume(name_container, self._state_EL[name_container][name_EL][2] )
            
            self._state_EL[name_container][name_EL][0].acquire()
            self._state_EL[name_container][name_EL][1] = state
            self._state_EL[name_container][name_EL][0].release()
            
            
        
        """return the value stocked in _state_EL without asking it to the arduino"""
    
    """do not use this function"""
    def _get_state_EL(self,name_container, name_EL):
        self._state_EL[name_container][name_EL][0].acquire()
        state = self._state_EL[name_container][name_EL][1]
        self._state_EL[name_container][name_EL][0].release() 
        return state
    
    """get state EL from arduino and set it in _state_EL"""
    def get_state_EL(self,name_container, name_EL): 
        """after each call to this function : be sure that it is different from NULL"""
        state = self.com_arduino.EL_read(name_container, name_EL)
        """if NULL, EL not connected"""
        
        self._set_state_EL(name_container, name_EL, state)
        return state
        
    """function to call each time something changes"""     
    def refresh_windows(self):
        if self.GUI :
            delta = time.time() -self.last_time
            if delta > 0.01 :
                """refresh the GUI"""
                #add in the thread of Tkinter the draw function
                #self.window.after(0,self.window.refresh)
                #self.window.after(0,self.window.refresh)
                #self.window.visual_feedback.after_idle(self.window.visual_feedback.draw)
                self.last_time = time.time()
        
                print("refresh") 
            
            #for item in self._state_pumps : 
                #print(self.get_state_pump(item))
            
        
    def set_BRBU_state(self, BU, state):
        """set the state of BU"""
        self._BRBU_state[BU][0].acquire()
        self._BRBU_state[BU][1] = state
        self._BRBU_state[BU][0].release()
        
    def get_BRBU_state(self, BU):
        """set the state of BU"""
        self._BRBU_state[BU][0].acquire()
        state = self._BRBU_state[BU][1]
        self._BRBU_state[BU][0].release()
        return state
    
    
    def get_formation_rate(self):
        """get the value of formation_rate"""
        self._formation_rate[0].acquire()
        value = self._formation_rate[1]
        self._formation_rate[0].release()
        return value
    
    def set_formation_rate(self, value):
        """set the value of formation_rate"""
        self._formation_rate[0].acquire()
        self._formation_rate[1] = value
        self._formation_rate[0].release()
    
    """not good solution, all action have to be listed in current_action in order to be stoped"""
    def set_keep_going(self, state):
        print("set keep going")
        if state : 
            print ("Actions Autorized")
        else : 
            print ("Actions Stopped") 
            for item in self._current_action : 
                self.set_current_action(item, state)
            
        self._keep_going[0].acquire()
        self._keep_going[1]  = state 
        self._keep_going[0].release()
        
    
    def get_keep_going(self):
        self._keep_going[0].acquire()
        value = self._keep_going[1] 
        self._keep_going[0].release()
        return value
    
    
    """set all action to False"""
    def stop_action(self):
        """rq : not used"""
        print ("Actions Stopped") 
        for item in self._current_action : 
            self.set_current_action(item, False)
    
    """ Set the states to the right values according to the log_start.txt file """
    def __setState__(self):
            # Open the file
        log_pin = open("config/config_start.txt", "r")
     
        # read the ligne one by one
        for ligne in log_pin:
            #Take out the end symbols (\n)
            ligne = ligne.strip()
            #split on  ":" 
            list = ligne.split(":")
            
            
            
            if list[0].strip() == "comments" :
                print (list[1].strip())
            
            elif list[0].strip() == "time_cycle" : 
                """set cycle's time { C1 : [Lock, 75] , C2 : ...} """
                self.time_cycle[list[1].strip()] = [threading.Lock(), float(list[2].strip())]
                print ("cycle "+ list[1].strip() +" set at " + list[2].strip())
                
                
            elif list[0].strip() =="occupied_volume" :
                """set the occupied volume { M1 : [Lock, 0.75] , C2 : ...} """
                self._occupied_volume[list[1].strip()] = [threading.Lock(), float(list[2].strip())]
                
            elif list[0].strip() =="number_usage" :
                """set the number_usage { BU1 : 0 , BU2 : 23, ...} """
                self.number_usage[list[1].strip()] = int(list[2].strip())
            
            elif list[0].strip() =="EL" :
                    
                    """Make a dictionnary of the EL for a container, then put it in the_EL :  {"AQ" : {"HIGH" : [threading.Lock(),False,1], "MEDIUM" : [threading.Lock(),False,0.66] },... } """
                    """if name_container not in the dict, we create a dictionnary for it in the_EL dictionnary"""
                    name_container =list[1].strip() 
                    name_EL = list[2].strip()
                    level_ref = list[3].strip()
                    if not name_container in self._state_EL :
                        self._state_EL[name_container] = {}
                    if level_ref == "NULL" : 
                        self._state_EL[name_container][name_EL] = [threading.Lock(),self.com_arduino.EL_read(name_container, name_EL),level_ref ]
                    else: 
                        self._state_EL[name_container][name_EL] = [threading.Lock(),self.com_arduino.EL_read(name_container, name_EL),float(level_ref) ]
    
    
    """check all the EL and set their state to their current state"""       
    def _check_all_EL(self):    
        for name_container in self.com_arduino.the_EL : 
            """name_container is for ex : "AQ" """
            for name_EL in self.com_arduino.the_EL[name_container] : 
                """name_EL is for ex "HIGH" """
                """if name container is not already in _state_EL, creation of a dictionnary at this key"""
                if not name_container in self._state_EL : 
                    self._state_EL[name_container] = {}
                self._state_EL[name_container][name_EL][1] = self.com_arduino.EL_read(name_container, name_EL)
    
    """kill all action running, st all pump to false"""          
    def kill_all(self):
        
        for item in self._current_action_evolved : 
            self.set_current_action_evolved(item, False)
        
        for item in self._current_action : 
            self.set_current_action(item, False)
        
        """set all the pump to false"""
        for item in self._state_pumps : 
            self.set_state_pump(item, False)
            
                
        
    
    """set the server to current_state"""
    def set_server(self, un_server):
        self.server = un_server
        
    """set the BRBU_controller to current_state"""
    def set_BRBU_controller(self, un_BRBU_controller):
        self.BRBU_controller = un_BRBU_controller
        
                    
    def set_windows(self,window):
        self.window = window
    
    def print_all_EL(self):
        for item in self._state_EL : 
            for i in self._state_EL[item] : 
                print(item + "_" + i + " : " + str(self._state_EL[item][i][1]))
        
        

        
    
