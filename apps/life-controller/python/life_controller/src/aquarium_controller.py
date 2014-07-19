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
    
        
        """actionning lift or not"""
        self.lift_action = True 
        self.time_wait_no_lift = 120
        
        self.start()
        
    def run(self):
        while True : 
            self._start_lock.acquire()
            if self._action_asked == "aquarium_cycle_light" : 
                self._aquarium_cycle_light()
            elif self._action_asked == "aquarium_cycle_heavy" : 
                self._aquarium_cycle_heavy()
                self.current_state._set_current_action_aquarium_evolved("aquarium_cycle_heavy", False)

    """start the action"""
    def start_aquarium_controller_action_name(self, action_name):
            self._action_asked = action_name
            self._start_lock.release()
 
 
    def _aquarium_cycle_light(self):
        """get the BU in use"""
        BU_USE = self.current_state.get_BU_USE()
        
        if BU_USE!= None : 
            self.current_state._set_current_action_aquarium_evolved("aquarium_cycle_light", True)
            self.current_state.saving_state_thread.write_action("Begin aquarium_cycle_light ")
            
            
            """cycle less that 1% of the aquarium at the end of each film"""
    
            
            """empty AQ for xx seconds, fill it until EL_HIGH with BU_USE"""
            action_name = "renew_light_AQ_" + BU_USE
            self.current_state.set_current_action_evolved(action_name, True)
            
            while self.current_state.get_current_action_evolved(action_name) and \
                self.current_state.get_current_action_aquarium_evolved("aquarium_cycle_light") : 
                time.sleep(1)
            
            
            
            
            if self.current_state.get_current_action_aquarium_evolved("aquarium_cycle_light") :
                """start filtration"""
                self.current_state.set_current_action("AQ_filtration", True)
            """lift_down"""
            
            if self.current_state.get_current_action_aquarium_evolved("aquarium_cycle_light") :
                if self.lift_action : 
                    self.current_state.set_current_action_lift_screen("lift_down")
                    """wait until lift_down is finished"""
                    
                    time.sleep(2)
                    while self.current_state.get_lift_busy() : 
                        time.sleep(2)
                    
                
                else : 
                    print("No lift, waiting " + str(self.time_wait_no_lift))
                    time.sleep(self.time_wait_no_lift)
            
            if self.current_state.get_current_action_aquarium_evolved("aquarium_cycle_light") :
                if self.lift_action : 
                    
                    """lift_up"""
                    
                    self.current_state.set_current_action_lift_screen("lift_up")
                    """wait until lift_up is finished"""
                    time.sleep(2)
                    while self.current_state.get_lift_busy() : 
                        time.sleep(2)
                
                else : 
                    print("No lift, waiting " + str(self.time_wait_no_lift))
                    time.sleep(self.time_wait_no_lift)
                
                
            
            
            """end filtration"""
            self.current_state.set_current_action("AQ_filtration", False)
            
            
            if False :
                """start the spectro and wait for a value"""
                current_concentration = self.current_state.get_spectro_mesure()
                
                print("current concentration AQ : " + str(current_concentration))
                self.current_state.set_inforamtion_asked("concentration", False)
            
            """function to call to save the state"""
            #self.current_state.saving_state()
            
            """end all that has been launched"""
            if not self.current_state.get_current_action_aquarium_evolved("aquarium_cycle_light") :
                print (action_name + " False")
                action_name = "renew_light_AQ_" + BU_USE
                self.current_state.set_current_action_evolved(action_name, False)
                 
                
            self.current_state._set_current_action_aquarium_evolved("aquarium_cycle_light", False)
            self.current_state.saving_state_thread.write_action("End aquarium_cycle_light ")
            
        else : 
            print ("No BU in USE")
                
    def _aquarium_cycle_heavy(self):
        
        """get the BU in use"""
        BU_USE = self.current_state.get_BU_USE()
        
        if BU_USE != None :
            self.current_state._set_current_action_aquarium_evolved("aquarium_cycle_heavy", True)
            self.current_state.saving_state_thread.write_action("Begin aquarium_cycle_heavy")
            """recycle 10% of the aquarium at the end of each film"""        
            
            """stop filtration"""
            self.current_state.set_current_action("AQ_filtration", True)
            
            if self.current_state.get_current_action_aquarium_evolved("aquarium_cycle_heavy") :
                if self.lift_action : 
                    """lift_down"""
                    self.current_state.set_current_action_lift_screen("lift_down")
                    time.sleep(2)
                    """wait until lift_down is finished"""
                    while self.current_state.get_lift_busy()  :  
                        time.sleep(2)
                else : 
                    print("No lift, waiting " + str(self.time_wait_no_lift))
                    time.sleep(self.time_wait_no_lift)
                
                
            """stop filtration"""
            self.current_state.set_current_action("AQ_filtration", False)
                
            
            """get the BU in use"""
            BU_USE = self.current_state.get_BU_USE()
            
            if self.current_state.get_current_action_aquarium_evolved("aquarium_cycle_heavy") :
                """start heavy renew"""
                action_name = "renew_heavy_AQ_" + BU_USE
                self.current_state.set_current_action_evolved(action_name, True)
                
                while self.current_state.get_current_action_evolved(action_name) and \
                self.current_state.get_current_action_aquarium_evolved("aquarium_cycle_heavy") : 
                    time.sleep(1)
                
            if self.current_state.get_current_action_aquarium_evolved("aquarium_cycle_heavy") :    
                """start filtration"""
                self.current_state.set_current_action("AQ_filtration", True)
            
            if self.current_state.get_current_action_aquarium_evolved("aquarium_cycle_heavy") :
                if self.lift_action : 
                    """lift_up"""
                    self.current_state.set_current_action_lift_screen("lift_up")
                    """wait until lift_down is finished"""
                    time.sleep(2)
                    while self.current_state.get_lift_busy() : 
                        time.sleep(2)
                else : 
                    print("No lift, waiting " + str(self.time_wait_no_lift))
                    time.sleep(self.time_wait_no_lift)
                
            """stop filtration"""
            self.current_state.set_current_action("AQ_filtration", False)
            
            """simplification"""
            if False : 
                """start the spectro and wait for a value"""
                current_concentration = self.current_state.get_spectro_mesure()
                print("current concentration AQ : " + str(current_concentration))
                
            if not self.current_state.get_current_action_aquarium_evolved("aquarium_cycle_heavy") :
                action_name = "renew_heavy_AQ_" + BU_USE
                self.current_state.set_current_action_evolved(action_name, False)
            
            self.current_state._set_current_action_aquarium_evolved("aquarium_cycle_heavy", False)
            self.current_state.saving_state_thread.write_action("End aquarium_cycle_heavy")
            
        else : 
            print ("No BU in USE")
                

        