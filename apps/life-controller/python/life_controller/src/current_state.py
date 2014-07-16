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
from action_thread.renew_heavy_AQ_BU import *
from action_thread.empty_BU_S import *
from action_thread.AQ_emptying import *
from time_controller import *

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
                             "P_FI_S" : [threading.Lock(),False], "P_SPECTRO" : [threading.Lock(),False] }
        
        """state of the EL {"AQ" : {"HIGH" : [threading.Lock(),False,1], "MEDIUM" : [threading.Lock(),False,0.66] },... }"""
        self._state_EL = dict()
        
        """state of Automatically checking the important values : ex EL_max"""
        self._security_checking = {"EL_max" : [threading.Lock(),False]}
        
        """Occupied volume for each container : { M1 : [Lock, 0.75] , M2 : ...} """
        self._occupied_volume = dict()
        
        """time of each cycle : { C1 : [Lock, 75] , C2 : ...}"""
        self.time_cycle = dict()
        
        """Number of usage for each BU : { BU1 : 0 , BU2 : 23, ...} """
        self.number_usage = dict()
        
        """BRBU_controller state"""
        self._BU_state = {"BU1" : [threading.Lock(), "NULL"],"BU2" : [threading.Lock(), "NULL"],"BU3" : [threading.Lock(), "NULL"] }
        
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
                                        "renew_heavy_AQ_BU1" : [threading.Lock(),False],\
                                        "renew_heavy_AQ_BU2" : [threading.Lock(),False],\
                                        "renew_heavy_AQ_BU3" : [threading.Lock(),False],\
                                 }
        """current_action_lift_screen"""
        self._current_action_lift_screen = {"lift_down" : [threading.Lock(),False],\
                                            "lift_up" : [threading.Lock(),False],\
                                            "screen_down_outside" : [threading.Lock(),False],\
                                            "screen_up_outside" : [threading.Lock(),False],\
                                            "screen_down_inside" : [threading.Lock(),False],\
                                            "screen_up_inside" : [threading.Lock(),False],\
                                            "lift_down_manual" : [threading.Lock(),False],\
                                            "lift_up_manual" : [threading.Lock(),False],\
                                            "screen_down_outside_manual" : [threading.Lock(),False],\
                                            "screen_up_outside_manual" : [threading.Lock(),False],\
                                            "screen_down_inside_manual" : [threading.Lock(),False],\
                                            "screen_up_inside_manual" : [threading.Lock(),False],\
                                            }
        
        """action on the aquarium"""
        self._current_action_aquarium_evolved = {"aquarium_cycle_light": [threading.Lock(),False],\
                                                 "aquarium_cycle_heavy": [threading.Lock(),False],\
                                                 }
        """action on the aquarium"""
        self._current_action_aquarium = {"AQ_emptying_EL_HIGH": [threading.Lock(),False],\
                                         "AQ_emptying_EL_MIDDLE": [threading.Lock(),False],\
                                         "AQ_emptying_EL_LOW": [threading.Lock(),False],\
                                         }
        
        """film_state"""
        self._current_film_state = {"film" :[threading.Lock(), False]}
        
        
        
        self._current_time_controller_state = {"exposition" : [threading.Lock(), False], "AQ_cycle_heavy" : [threading.Lock(), False]}
        
        
        """current_spectro_state"""
        self._current_spectro_state = {"spectro" : [threading.Lock(),False]}
         
        """current_light_state"""                               
        self._current_light_state = {"spectro_light" : [threading.Lock(),False]}
        
        
        """BRBU_controller state : true if it is running"""
        self._BRBU_controller_state = {"run" : [threading.Lock(),False],\
                                       "pause" : [threading.Lock(),False]}
        
        
        """AQ_concentration"""
        self._concentration = {"AQ" :[threading.Lock(), 0]}
        
        
        
        """time since last resfresh of the GUI"""
        self._GUI_last_time = time.time()
        
        self._formation_rate = [threading.Lock(), 35]
        
        """list of server in charge of the communication"""
        self._client_connected = {"server_formation_rate" : [threading.Lock(), None, False,"formation_rate"],\
                                 "server_level" : [threading.Lock(), None, False,"level"],\
                                 "server_level_AQ" : [threading.Lock(), None, False,"level_AQ"],\
                                 "server_concentration" : [threading.Lock(), None, False,"concentration"],\
                                 "server_arduino_order" : [threading.Lock(), None, False,"arduino"]}
        
        """list of information asked : name : [lock, state, name_server] """
        self._information_asked = {"formation_rate" : [threading.Lock(), False,"server_formation_rate" ],\
                                   "level" : [threading.Lock(), False, "server_level"],\
                                   "level_AQ" : [threading.Lock(), False, "server_level_AQ"],\
                                   "concentration" : [threading.Lock(), False,"server_concentration"]}
      
        
        """lock, state, day, in order to know if these action have been done yet"""
        self._daily_action = {"AQ_cycle_heavy" : [threading.Lock(), False, 0]}
        
        """if there is a GUI or not"""
        self.GUI = False 
        
        "emergency stop "  
        self._keep_going = [threading.Lock(), True]

        

        
        """initialize all values after a log_start.txt"""
        self.__setState__()
        #self._check_all_EL()
    
        #self._client_connected = 
    
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
        
    def P_SPECTRO(self, state):
        name = 'P_SPECTRO'
        self.set_state_pump( name, state )
          
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
        
    """ACTION"""
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
      
    """use this function to launch an action :    
    action possible : ..."""
    def set_current_action(self, name, state):
        """check if there is no action running"""
        b = True
        for item in self._current_action : 
            if not item == name :  
                if self.get_current_action(item) : 
                    b = False
        
        """if there is no action running"""
        # if b :
        #     if not self.get_current_action(name) == state : 
        #         if name == "AQ_filtration" : 
        #             if state : 
        #                 """start the thread to for a filtration, only if there is no filtration at the same time"""
        #                 if not self.get_current_action("AQ_filtration") :
        #                     action = AQ_filtration(self)
        #                     action.start()
        #             else : 
        #                 """set the action to end, and will stop the current action""" 
        #                 self._set_current_action("AQ_filtration",False)
                        
        #         elif name == "fill_BU1_AQ" : 
        #             if state : 
        #                 """start the thread to for a filtration, only if there is no filtration at the same time"""
        #                 if not self.get_current_action("fill_BU1_AQ") :
        #                     action = fill_BU_AQ(self,"BU1")
        #                     action.start()
                        
        #             else : 
        #                 self._set_current_action("fill_BU1_AQ",False)
        #         elif name == "fill_BU2_AQ" : 
        #             if state : 
        #                 """start the thread to for a filtration, only if there is no filtration at the same time"""
        #                 if not self.get_current_action("fill_BU2_AQ") :
        #                     action = fill_BU_AQ(self,"BU2")
        #                     action.start()
                        
        #             else : 
        #                 self._set_current_action("fill_BU2_AQ",False)
        #         elif name == "fill_BU3_AQ" :
        #             if state : 
        #                 """start the thread to for a filtration, only if there is no filtration at the same time"""
        #                 if not self.get_current_action("fill_BU3_AQ") :
        #                     action = fill_BU_AQ(self,"BU3")
        #                     action.start()
        #             else : 
        #                 self._set_current_action("fill_BU3_AQ",False)
                
        #         elif name == "empty_BU1_S" :
        #             if state : 
        #                 """start the thread for a emptying, only if there is no filtration at the same time"""
        #                 if not self.get_current_action("empty_BU1_S") :
        #                     action = empty_BU_S(self,"BU1")
        #                     action.start()
        #             else : 
        #                 self._set_current_action("empty_BU1_S",False)
                
        #         elif name == "empty_BU2_S" :
        #             if state : 
        #                 """start the thread to for a filtration, only if there is no filtration at the same time"""
        #                 if not self.get_current_action("empty_BU2_S") :
        #                     action = empty_BU_S(self,"BU2")
        #                     action.start()
        #             else : 
        #                 self._set_current_action("empty_BU2_S",False)
                
        #         elif name == "empty_BU3_S" :
        #             if state : 
        #                 """start the thread to for a filtration, only if there is no filtration at the same time"""
        #                 if not self.get_current_action("empty_BU3_S") :
        #                     action = empty_BU_S(self,"BU3")
        #                     action.start()
        #             else : 
        #                 self._set_current_action("empty_BU3_S",False)
        if b :
            if not self.get_current_action(name) == state : 
                if name == "AQ_filtration" : 
                     
                    self.set_state_pump("P_AQ_FI", state)
                    self.set_state_pump("P_FI_AQ_1", state)
                    self.set_state_pump("P_FI_AQ_3", state)
                    self._set_current_action("AQ_filtration",state)
                    
                    
                 
                        
                elif name == "fill_BU1_AQ" : 
                    self.set_state_pump("P_BU1_FI", state)
                    self.set_state_pump("P_FI_AQ_1", state)
                    self._set_current_action("fill_BU1_AQ",state)

                elif name == "fill_BU2_AQ" : 
                    self.set_state_pump("P_BU2_FI", state)
                    self.set_state_pump("P_FI_AQ_1", state)
                    self._set_current_action("fill_BU2_AQ",state)
               
                elif name == "fill_BU3_AQ" :
                    self.set_state_pump("P_BU3_FI", state)
                    self.set_state_pump("P_FI_AQ_1", state)
                    self._set_current_action("fill_BU3_AQ",state)

                elif name == "empty_BU1_S" :
                    self.set_state_pump("P_BU1_FI", state)
                    self.set_state_pump("P_FI_S", state)
                    self._set_current_action("empty_BU1_S",state)
                
                elif name == "empty_BU2_S" :
                    self.set_state_pump("P_BU2_FI", state)
                    self.set_state_pump("P_FI_S", state)
                    self._set_current_action("empty_BU2_S",state)
                
                elif name == "empty_BU3_S" :
                    self.set_state_pump("P_BU3_FI", state)
                    self.set_state_pump("P_FI_S", state)
                    self._set_current_action("empty_BU3_S",state)
        else : 
            print(name + " to "+ str(state) + " impossible : already a task running")                
    
    """do not use this function"""       
    def _set_current_action(self, name, state):
        self._current_action[name][0].acquire()
        self._current_action[name][1] = state
        self._current_action[name][0].release()
    
    def get_current_action(self, name):
        self._current_action[name][0].acquire()
        state = self._current_action[name][1]
        self._current_action[name][0].release()
        return state   
    
    """LIFT ORDERS"""   
    """Automatic Order to liftDown and liftUp, screenDown and screenUp"""
    
    def lift_down(self):
        print("lift_down")
        self.set_current_action_lift_screen("lift_down")

    def lift_up(self):
        print("lift_up")
        self.set_current_action_lift_screen("lift_up")

    def screen_down_outside(self):
        print("screen_down_outside")
        self.set_current_action_lift_screen("screen_down_outside")

    def screen_up_outside(self):
        print("screen_up_outside")
        self.set_current_action_lift_screen("screen_up_outside")
    
    def screen_down_inside(self):
        print("screen_down_inside")
        self.set_current_action_lift_screen("screen_down_inside")

    def screen_up_inside(self):
        print("screen_up_inside")
        self.set_current_action_lift_screen("screen_up_inside")
    

    """Manual Order to liftDown and liftUp, screenDown and screenUp"""
    def lift_down_manual(self):
        print("lift_down_manual")
        self.set_current_action_lift_screen("lift_down_manual")

    def lift_up_manual(self):
        print("lift_up_manual")
        self.set_current_action_lift_screen("lift_up_manual")

    def screen_down_outside_manual(self):
        print("screen_down_outside_manual")
        self.set_current_action_lift_screen("screen_down_outside_manual")

    def screen_up_outside_manual(self):
        print("screen_up_outside_manual")
        self.set_current_action_lift_screen("screen_up_outside_manual")
    
    def screen_down_inside_manual(self):
        print("screen_down_inside_manual")
        self.set_current_action_lift_screen("screen_down_inside_manual")

    def screen_up_inside_manual(self):
        print("screen_up_inside_manual")
        self.set_current_action_lift_screen("screen_up_inside_manual")
        
        """checking if there is not already a task runnig on this arduino"""
    def get_lift_busy(self):
        b = False
        for item in self._current_action_lift_screen :   
            if self.get_current_action_lift_screen(item) : 
                b = True
        return b
    
    def set_current_action_lift_screen(self, name):
        """checking if there is not already a task runnig on this arduino"""
        b = True
        for item in self._current_action_lift_screen : 
            if not item == name :  
                if self.get_current_action_lift_screen(item) : 
                    b = False
        """if there is no action running"""
        if b : 
            if name == "lift_down": 
                answer = self.com_arduino.lift_down()
            elif name == "lift_up": 
                answer = self.com_arduino.lift_up()  
            elif name == "screen_down_outside": 
                answer = self.com_arduino.screen_down_outside() 
            elif name == "screen_up_outside": 
                answer = self.com_arduino.screen_up_outside()
            elif name == "screen_down_inside": 
                answer = self.com_arduino.screen_down_inside() 
            elif name == "screen_up_inside": 
                answer = self.com_arduino.screen_up_inside() 
            elif name == "lift_down_manual": 
                answer = self.com_arduino.lift_down_manual() 
            elif name == "lift_up_manual": 
                answer = self.com_arduino.lift_up_manual()  
            elif name == "screen_down_outside_manual": 
                answer = self.com_arduino.screen_down_outside_manual() 
            elif name == "screen_up_outside_manual": 
                answer = self.com_arduino.screen_up_outside_manual()
            elif name == "screen_down_inside_manual": 
                answer = self.com_arduino.screen_down_inside_manual() 
            elif name == "screen_up_inside_manual": 
                answer = self.com_arduino.screen_up_inside_manual() 
                
        """value in _current_action_lift_screen is set to Tru by arduino_lift_thread"""
            

        
    """do not use this function"""       
    def _set_current_action_lift_screen(self, name, state):
        self._current_action_lift_screen[name][0].acquire()
        self._current_action_lift_screen[name][1] = state
        self._current_action_lift_screen[name][0].release()
    
    def get_current_action_lift_screen(self, name):
        self._current_action_lift_screen[name][0].acquire()
        state = self._current_action_lift_screen[name][1]
        self._current_action_lift_screen[name][0].release()
        return state   
    
    """EVOLVED ACTION AQ"""
    def set_current_action_aquarium_evolved(self, name, state):
        if not self.get_current_action_aquarium_evolved(name) == state : 
            """check if there is no action running"""
            if self.get_security_checking("EL_max") : 
                b = True
                for item in self._current_action_evolved : 
                    if not item == name :
                        if self.get_current_action_evolved(item) : 
                            b = False
                """if there is no action running"""
                if b : 
                    self._set_current_action_aquarium_evolved(name, state)
                    if state : 
                        self.aquarium_controller.start_aquarium_controller_action_name(name)
                        
                   
        
    def _set_current_action_aquarium_evolved(self, name, state):
        self._current_action_aquarium_evolved[name][0].acquire()
        self._current_action_aquarium_evolved[name][1] = state
        self._current_action_aquarium_evolved[name][0].release()

        
    def get_current_action_aquarium_evolved(self, name):    
        self._current_action_aquarium_evolved[name][0].acquire()
        state = self._current_action_aquarium_evolved[name][1]
        self._current_action_aquarium_evolved[name][0].release()
        return state
    
    """ ACTION AQ:
    'AQ_emptying_EL_MIDDLE'
    'AQ_emptying_EL_LOW' """
    def set_current_action_aquarium(self, name, state):
        if not self.get_current_action_aquarium(name) == state : 
            if not self.get_current_action_aquarium_evolved(name) == state : 
                """check if there is no action running"""
                b = True
                for item in self._current_action_evolved : 
                    if not item == name :
                        if self.get_current_action_evolved(item) : 
                            b = False
                """if there is no action running"""
                if b :  
                    if state :
                        if name == "AQ_emptying_EL_MIDDLE" : 
                            action =  AQ_emptying("MIDDLE")
                            action.start()
                        elif name == "AQ_emptying_EL_LOW" : 
                            action =  AQ_emptying("LOW")
                            action.start()
                        elif name == "AQ_emptying_EL_HIGH" : 
                            action =  AQ_emptying("HIGH")
                            action.start()
                    else : 
                        self._set_current_action_aquarium(name, False)
                    
    def _set_current_action_aquarium(self, name, state):
        self._current_action_aquarium[name][0].acquire()
        self._current_action_aquarium[name][1] = state
        self._current_action_aquarium[name][0].release()

        
    def get_current_action_aquarium(self, name):    
        self._current_action_aquarium[name][0].acquire()
        state = self._current_action_aquarium[name][1]
        self._current_action_aquarium[name][0].release()
        return state
        
    """FILM STATE"""
    
    def set_current_film_state(self, name, state,):
        if not self.get_current_film_state(name) == state : 
            self._set_current_film_state(name, state)
            if state : 
                self.seance_controller.start_film()
                
                
                
    
    """do not use this function"""       
    def _set_current_film_state(self, name, state):
        self._current_film_state[name][0].acquire()
        self._current_film_state[name][1] = state
        self._current_film_state[name][0].release()
    
    def get_current_film_state(self, name):
        self._current_film_state[name][0].acquire()
        state = self._current_film_state[name][1]
        self._current_film_state[name][0].release()
        return state   
    
    """LIGHT """
    
    def set_current_light_state(self, name, state,):
        """if different from current state"""
        if not self.get_current_light_state(name) == state : 
            """checking if there is not already a task runnig on this arduino"""
            if name == "spectro_light": 
                self.com_arduino.spectro_light(state)
                self._set_current_light_state(name, state)
                
    
    """do not use this function"""       
    def _set_current_light_state(self, name, state):
        self._current_light_state[name][0].acquire()
        self._current_light_state[name][1] = state
        self._current_light_state[name][0].release()
    
    def get_current_light_state(self, name):
        self._current_light_state[name][0].acquire()
        state = self._current_light_state[name][1]
        self._current_light_state[name][0].release()
        return state   
    
    """SECURITY CHECKING"""

    """set the checking to True or False : security system name : 
        - EL_max"""       
    def set_security_checking(self, name, state):
        """if state asked is different from current_state"""
        if not self.get_security_checking(name) == state : 
            """start"""
            if state : 
                self.security_EL.lock_start.release()
                self._set_security_checking(name, True)
                """stop"""
            else : 
                self.security_EL.lock_start.acquire()
                self._set_security_checking(name, False)
                
    """do not use this function"""       
    def _set_security_checking(self, name, state):
        self._security_checking[name][0].acquire()
        self._security_checking[name][1] = state
        self._security_checking[name][0].release()
    
    def get_security_checking(self, name):
        self._security_checking[name][0].acquire()
        state = self._security_checking[name][1]
        self._security_checking[name][0].release()
        return state
    
    """SPECTRO"""
    
    """function to cal to turn on the spectro, wait until the value is established and return it"""
    def get_spectro_mesure(self):
        """turn on the spectro"""
        self.set_current_spectro_state("spectro",True)
        """wait some time before"""
        while self.get_concentration("AQ")=="NULL" : 
                time.sleep(1)
                print("spectro wait")
        value = self.get_concentration("AQ")
        self.set_current_spectro_state("spectro",False)
        return value 
       
        
        
    def set_current_spectro_state(self, name, state,):
        """if different from current state"""
        if not self.get_current_spectro_state(name) == state : 
            
            """checking if there is not already a task runnig on this arduino"""
            if name == "spectro": 
                self.set_current_light_state("spectro_light", state)
                self.set_state_pump("P_SPECTRO", state)
                self.set_information_asked("concentration", state)
                self._set_current_spectro_state(name, state)
    
    
            
            
    """do not use this function"""       
    def _set_current_spectro_state(self, name, state):
        self._current_spectro_state[name][0].acquire()
        self._current_spectro_state[name][1] = state
        self._current_spectro_state[name][0].release()
    
    def get_current_spectro_state(self, name):
        self._current_spectro_state[name][0].acquire()
        state = self._current_spectro_state[name][1]
        self._current_spectro_state[name][0].release()
        return state   
    
    """EVOLVED ACTION""" 
    
    """use this function to launch an evolved action :    
    action possible : 
    auto_AQ_filtration 
    renew_light_AQ_BU1 
    renew_light_AQ_BU2
    renew_light_AQ_BU3 """
    
    def renew_light_AQ(self, name,name_BU, state):
        name_action = "renew_light_AQ_"+name_BU
        self.set_current_action_evolved(name_action)
    
    def set_current_action_evolved(self, name, state):
        if not self.get_current_action_evolved(name) == state :
            """if false"""
            if not state :
                self._set_current_action_evolved(name,False) 
                
                """if trying to begin an action"""
            else : 
                """check if there is no action running"""
                b = True
                for item in self._current_action_evolved : 
                    if not item == name :
                        if self.get_current_action_evolved(item) : 
                            b = False
                """if there is no action running"""
                if b and self.get_security_checking("EL_max"): 
             
                    if name == "auto_AQ_filtration" : 
                        action = auto_AQ_filtration(self)
                        action.start()
                                
                    if name == "renew_light_AQ_BU1" : 
                         
                        action = renew_light_AQ_BU(self,"BU1")
                        action.start()
                        
                    if name == "renew_light_AQ_BU2" : 
                      
                        action = renew_light_AQ_BU(self,"BU2")
                        action.start() 
                       
                    if name == "renew_light_AQ_BU3" : 
                    
                        action = renew_light_AQ_BU(self,"BU3")
                        action.start()  
                        
                    if name == "renew_heavy_AQ_BU1" : 
                        
                        action = renew_heavy_AQ_BU(self,"BU1")
                        action.start()
                                
                      
                    if name == "renew_heavy_AQ_BU2" : 
                       
                        action = renew_heavy_AQ_BU(self,"BU2")
                        action.start()
                            
                       
                    if name == "renew_heavy_AQ_BU3" : 
                      
                        action = renew_heavy_AQ_BU(self,"BU3")
                        action.start()
                  
        else : 
            print("already a evolved task running")   
        
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

    
    
    
    """VOLUME"""
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
        

    """CONCENTRATION"""  
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
        
      
    """ELECTRODES""" 
    
    """get state EL from arduino and set it in _state_EL"""
    def get_state_EL(self,name_container, name_EL): 
        """WARING BR3, MAX is disabled"""
        if name_container == "BR3" and name_EL == "MAX" : 
            state = False
        else : 
            
            """after each call to this function : be sure that it is different from NULL"""
            state = self.com_arduino.EL_read(name_container, name_EL)
            """if NULL, EL not connected"""
        
        """f state == NULL, do not updtate _EL_state"""
        if not state == "NULL" : 
            self._set_state_EL(name_container, name_EL, state)
        
        return state
    
     
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
    
    """do not use this function, use get_state_EL"""
    def _get_state_EL(self,name_container, name_EL):
        self._state_EL[name_container][name_EL][0].acquire()
        state = self._state_EL[name_container][name_EL][1]
        self._state_EL[name_container][name_EL][0].release() 
        return state
    
    """check all the EL and set their state to their current state"""       
    def _check_all_EL(self):    
        for name_container in self._state_EL : 
            """name_container is for ex : "AQ" """
            for name_EL in self._state_EL[name_container] : 
                """name_EL is for ex "HIGH" """
                """if name container is not already in _state_EL, creation of a dictionnary at this key"""
                if not name_container in self._state_EL : 
                    self._state_EL[name_container] = {}
                self._state_EL[name_container][name_EL][1] = self.com_arduino.EL_read(name_container, name_EL)
    
    def print_all_EL(self):
        """refresh all EL before printing them"""
        self._check_all_EL()
        print ("EL state : ")
        for item in self._state_EL : 
            for i in self._state_EL[item] : 
                print("EL  : "  + item + " : " + i + " : " + str(self._state_EL[item][i][1]))
    
        print("\n")
    
    """INFORMATION ASKED"""
    
    """use this function to ask information"""
    def set_information_asked(self, name, state):
        """set the state of BU"""
        """if asked different from current state"""
        if not self.get_information_asked(name) == state : 
            """checking if the client is connected"""
            server_name = self.get_information_asked_server(name)
            if self.get_client_connected_state(server_name) :
                """if OK"""
                self.get_client_connected(server_name).ask_information(state)
                self._set_information_asked(name, state)
                """set concentration to NULL each time we ask information about concentrtion"""
                if name =="concentration" and state : 
                    self.set_concentration("AQ", "NULL")
            else : 
                print("information asked : " + name + " " + str(state) + " failed : " +  server_name + " not connected") 
            
        
    """do not use this function"""
    def _set_information_asked(self, name, state):
        """set the state of information aksed"""
        self._information_asked[name][0].acquire()
        self._information_asked[name][1] = state
        self._information_asked[name][0].release()
        
    """get the state of information aksed :formation_rate, level, concentration """   
    def get_information_asked(self, name):
        self._information_asked[name][0].acquire()
        state = self._information_asked[name][1]
        self._information_asked[name][0].release()
        return state

    """get the name of the server associated to the information aksed  """   
    def get_information_asked_server(self, name):
        self._information_asked[name][0].acquire()
        n = self._information_asked[name][2]
        self._information_asked[name][0].release()
        return n
     
    """BU_STATE""" 
    """get the BU in USE state"""
    def get_BU_USE(self):
        for item in self._BU_state : 
            if self.get_BU_state(item) == "USE" : 
                return item
    
    """set the state of each BU : WAIT, USE, EMPTY, or NULL if no status"""  
    def set_BU_state(self, BU, state):
        """set the state of BU"""
        self._BU_state[BU][0].acquire()
        self._BU_state[BU][1] = state
        self._BU_state[BU][0].release()
    
    """get the state of BU"""    
    def get_BU_state(self, BU):
        self._BU_state[BU][0].acquire()
        state = self._BU_state[BU][1]
        self._BU_state[BU][0].release()
        return state
    
    """BRBU_COTROLLER"""
    
    
    """Use it to start/stop or pause/restart a cycle of BRBU : 
    type : run, pause """
    def set_BRBU_controller_state(self, type,  state) : 
        """if not already in the same state"""
        if not self.get_BRBU_controller_state(type) == state :
            if type == "run" : 
                """get out from pause mode"""
                self.set_BRBU_controller_state("pause",False)
                
                """start"""
                if state : 
                    """set self.stop to False, in order to pursue """
                    self._set_BRBU_controller_state("run", True)
                    if not self.BRBU_controller.auto_start : 
                        self.BRBU_controller._reset_time()
                    self.BRBU_controller.lock_start.release()
    
                    """Stop"""   
                else : 
                    self._set_BRBU_controller_state("run",False)
                    self.BRBU_controller._reset_time()
                    
            if type == "pause" :
                """if not stopped"""
                if self.get_BRBU_controller_state("run") : 
                    """if order different from current state"""
                    
                    if state == True : 
                        """get in the mode pause"""
                        self.BRBU_controller._lock_pause.acquire()
                        self._set_BRBU_controller_state("pause",True)
                    
                        """if False : get out from the pause"""
                    else : 
                        """exit pause mode only if EL_max is active"""
                        if self.get_security_checking("EL_max") : 
                            self.BRBU_controller._lock_pause.release()
                            self._set_BRBU_controller_state("pause",False)
        
    """do not use this function"""
    def _set_BRBU_controller_state(self, type, state) : 
        self._BRBU_controller_state[type][0].acquire()
        self._BRBU_controller_state[type][1] = state 
        self._BRBU_controller_state[type][0].release()
    
    """get the status of  BRBU_controller : True if cycle is running, false otherwise : 
    initial condition : """
    def get_BRBU_controller_state(self, type):
        self._BRBU_controller_state[type][0].acquire()
        state =  self._BRBU_controller_state[type][1] 
        self._BRBU_controller_state[type][0].release()
        return state
    
    """CLIENT CONNECTED"""
    
    """set the state of a server"""
    def set_client_connected_state(self, type, state) :
        """if false : set the information asked associated to the client to false"""
        if not state : 
            """if different from arduino, because arduino for test_mode"""
            if not self.get_client_connected_information_asked(type) =="arduino" : 
                self.set_information_asked(self.get_client_connected_information_asked(type), False)
         
        self._client_connected[type][0].acquire()
        self._client_connected[type][2] = state
        self._client_connected[type][0].release()
        
        
        
        
        
     
        
    """set the actual server"""
    def set_client_connected(self, type, server) : 
        self._client_connected[type][0].acquire()
        self._client_connected[type][1] = server 
        self._client_connected[type][0].release()
    
    """get information_asked associated to the client"""
    def get_client_connected_information_asked(self, type):
        self._client_connected[type][0].acquire()
        information_asked =  self._client_connected[type][3] 
        self._client_connected[type][0].release()
        return information_asked
    
    """get the actual server"""""
    def get_client_connected(self, type):
        self._client_connected[type][0].acquire()
        server =  self._client_connected[type][1] 
        self._client_connected[type][0].release()
        return server
    """set the status server"""
    def get_client_connected_state(self, type):
        self._client_connected[type][0].acquire()
        state =  self._client_connected[type][2] 
        self._client_connected[type][0].release()
        return state
    
    """FORMATION RATE"""
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
    
    """DAILY ACTION"""
    def get_daily_action_state(self, name):
        """get the value of formation_rate"""
        self._daily_action[name][0].acquire()
        value = self._daily_action[name][1]
        self._daily_action[name][0].release()
        return value
    
    def get_daily_action_day(self, name):
        """get the value of formation_rate"""
        self._daily_action[name][0].acquire()
        day = self._daily_action[name][2]
        self._daily_action[name][0].release()
        return day
    
    def set_daily_action_state(self, name, state):
        """set the value of formation_rate"""
        self._daily_action[name][0].acquire()
        self._daily_action[name][1] = state
        self._daily_action[name][0].release()
    
    def set_daily_action_day(self, name, day):
        """set the value of formation_rate"""
        self._daily_action[name][0].acquire()
        self._daily_action[name][2] = day
        self._daily_action[name][0].release()
    
    
    
    """EMERGENCY ACTIONS"""
    
    
    
    """kill all action running, st all pump to false"""          
    def kill_all(self):
        
        self.set_BRBU_controller_state("pause",True)
        
        for item in self._current_action_evolved : 
            self.set_current_action_evolved(item, False)
        
        for item in self._current_action : 
            self.set_current_action(item, False)
        
        """set all the pump to false"""
        for item in self._state_pumps : 
            self.set_state_pump(item, False)
        
        for item in self._current_light_state : 
            self.set_current_light_state(item, False)
            
        for item in self._current_spectro_state : 
            self.set_current_spectro_state(item, False)
            
        for item in self._current_spectro_state : 
            self.set_current_spectro_state(item, False)
        
        for item in self._current_action_aquarium : 
            self.set_current_action_aquarium(item, False)
            
        for item in self._current_action_aquarium_evolved : 
            self.set_current_action_aquarium_evolved(item, False)
            
        for item in self._current_action_aquarium_evolved : 
            self.set_current_action_aquarium_evolved(item, False)
        
        for item in self._current_film_state : 
            self.set_current_film_state(item, False)
                
        for item in self._current_time_controller_state : 
            self.set_current_time_controller_state(item, False)
                
        for item in self._current_spectro_state : 
            self.set_current_spectro_state(item, False)
                
        for item in self._current_light_state : 
            self.set_current_light_state(item, False)
                
        
    
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
            
    
    """READING CONFIGURATIONS SCRIPTS"""
    """ Set the states to the right values according to the log_start.txt file """
    def __setState__(self):
            # Open the file
        start_file = open("config/config_start.txt", "r")
     
        # read the ligne one by one
        for ligne in start_file:
            #Take out the end symbols (\n)
            ligne = ligne.strip()
            #split on  ":" 
            list = ligne.split(":")
            
            
            
            if list[0].strip() == "comments" :
                continue
            
            elif list[0].strip() == "print" :
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
    
        start_file.close()
        
        last_state_file = open("save_current_situation/last_state.txt", "r")
        
        for lign in last_state_file:
            #Take out the end symbols (\n)
            lign = lign.strip()
            #split on  ":" 
            list = lign.split(":")
            
            
            
            if list[0].strip() == "comments" :
                continue
            
            elif list[0].strip() == "print" :
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
                
            elif list[0].strip() =="daily_action" :
                """set the number_usage { BU1 : 0 , BU2 : 23, ...} """
                name_action = list[1].strip()
                print(name_action)
                if list[2].strip() =="True" : 
                    state_action = True
                else : 
                    state_action = False
                day_action = int(list[3].strip())
                self.set_daily_action_state(name_action,state_action)
                self.set_daily_action_day(name_action,day_action)   
                
                
            
            
        last_state_file.close()
        
    
    """Time_controller"""
    
    def set_current_time_controller_state(self, name, state):
        """set the value of formation_rate"""
        if  not (self.get_current_time_controller_state( name) == state) :
                self._set_current_time_controller_state(name, state)
                           
    def _set_current_time_controller_state(self, name, state):
        """set the value of formation_rate"""
        self._current_time_controller_state[name][0].acquire()
        self._current_time_controller_state[name][1] = state
        self._current_time_controller_state[name][0].release()
    
    def get_current_time_controller_state(self, name):
        
        """set the value of formation_rate"""
        self._current_time_controller_state[name][0].acquire()
        state = self._current_time_controller_state[name][1] 
        self._current_time_controller_state[name][0].release()
        return state
            
                
        
    """SETTING OBJECT IN ATTRIBUTE"""
    """set the server to current_state"""
    def set_server(self, un_server):
        self.server = un_server
        
    """set the BRBU_controller to current_state"""
    def set_BRBU_controller(self, un_BRBU_controller):
        self.BRBU_controller = un_BRBU_controller
        
                    
    def set_windows(self,window):
        self.window = window
        
    def set_security_EL(self, un_security_EL):
        self.security_EL = un_security_EL
         
    def set_config_manager(self, a_config_manager):
        self.config_manager = a_config_manager
        
    def set_seance_controller(self, un_seance_controller):
        self.seance_controller = un_seance_controller
        
    def set_aquarium_controller(self, un_aquarium_controller):
        self.aquarium_controller = un_aquarium_controller
        
    def set_saving_state_thread(self, un_saving_state_thread):
        self.saving_state_thread = un_saving_state_thread
    
    """function to call each time something changes"""     
    def refresh_windows(self):
        if self.GUI :
            delta = time.time() -self._GUI_last_time
            if delta > 0.01 :
                """refresh the GUI"""
                #add in the thread of Tkinter the draw function
                #self.window.refresh()
                #self.window.after(0,self.window.refresh)
                #self.window.visual_feedback.after_idle(self.window.visual_feedback.draw)
                self._GUI_last_time = time.time()
        
                #print("refresh") 
            
            #for item in self._state_pumps : 
                #print(self.get_state_pump(item)) 
        
        

        
    
