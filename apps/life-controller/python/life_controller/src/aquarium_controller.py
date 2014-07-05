'''
Created on 11 mai 2014

@author: ensadlab
'''
import time
from com_arduino import *
from current_state import *

class aquarium_controller(threading.Thread):
    '''
    manage the aquarium
    '''


    def __init__(self, un_current_state):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        self.current_state = un_current_state
        
        self._action_asked = None
        
        self._start_lock = threading.Lock()
        self._start_lock.acquire()
    
        self.start()
        
    def run(self):
        while True : 
            self._start_lock.acquire()
            if self._action_asked == "aquarium_cycle_light" : 
                self.aquarium_cycle_light()
            elif self._action_asked == "aquarium_cycle_heavy" : 
                self.aquarium_cycle_light()

    """start the action"""
    def start_aquarium_controller_action_name(self, action_name):
            self._action_asked = action_name
            self._start_lock.release()
 
 
    def aquarium_cycle_light(self):
        
       
        self.current_state._set_current_action_aquarium_evolved("aquarium_cycle_light", True)
        """cycle less that 1% of the aquarium at the end of each film"""
        
        """get the BU in use"""
        BU_USE = self.current_state.get_BU_USE()
        
        """empty AQ for xx seconds, fill it until EL_HIGH with BU_USE"""
        action_name = "renew_light_AQ_" + BU_USE
        self.current_state.set_current_action_evolved(action_name, True)
        
        while self.current_state.get_current_action_evolved(action_name) : 
            time.sleep(1)
        
        
        """start filtration"""
        self.current_state.set_current_action("AQ_filtration", True)
        """lift_down"""
        self.current_state._current_action_lift_screen("lift_down")
        """wait until lift_down is finished"""
        while self.current_state.get_lift_busy() : 
            time.sleep(2)
        """lift_up"""
        self.current_state._current_action_lift_screen("lift_up")
        """wait until lift_up is finished"""
        while self.current_state.get_lift_busy() : 
            time.sleep(2)
        
        """end filtration"""
        self.current_state.set_current_action("AQ_filtration", False)
        
        
        """start the spectro and wait for a value"""
        self.current_state.set_information_asked("concentration", True)
        while self.current_state.get_spectro_mesure()=="NULL" : 
            time.sleep(1)
        current_concentration = self.current_state.get_spectro_mesure()
        
        print("current concentration AQ : " + str(current_concentration))
        self.current_state.set_inforamtion_asked("concentration", False)
        
        """function to call to save the state"""
        #self.current_state.saving_state()

        self.current_state._set_current_action_aquarium_evolved("aquarium_cycle_light", False)
    
    def aquarium_cycle_heavy(self):
        """recycle 10% of the aquarium at the end of each film"""
        
        self.current_state._set_current_action_aquarium_evolved("aquarium_cycle_heavy", True)
        
        
        
        """lift_down"""
        self.current_state._current_action_lift_screen("lift_down")
        
        """wait until lift_down is finished"""
        while self.current_state.get_lift_busy()  :  
            time.sleep(2)
            
        """stop filtration"""
        self.current_state.set_current_action("AQ_filtration", False)
            
        
        """get the BU in use"""
        BU_USE = self.current_state.get_BU_USE()
        
        """start heavy renew"""
        action_name = "renew_heavy_AQ_" + BU_USE
        self.current_state.set_current_action_evolved(action_name, True)
        
        while self.current_state.get_current_action_evolved(action_name) : 
            time.sleep(1)
        
        """start filtration"""
        self.current_state.set_current_action("AQ_filtration", True)
        
        """lift_up"""
        self.current_state._current_action_lift_screen("lift_up")
        """wait until lift_down is finished"""
        while self.current_state.get_lift_busy() : 
            time.sleep(2)
            
        """stop filtration"""
        self.current_state.set_current_action("AQ_filtration", False)
        
        
        """start the spectro and wait for a value"""
        self.current_state.set_information_asked("concentration", True)
        while self.current_state.get_spectro_mesure()=="NULL" : 
            time.sleep(1)
        current_concentration = self.current_state.get_spectro_mesure()
        print("current concentration AQ : " + str(current_concentration))

        self.current_state._set_current_action_aquarium_evolved("aquarium_cycle_heavy", False)
        

        
         
            

        