'''
Created on Apr 27, 2014

@author: Cactus
'''

import threading
import time

class current_state(object):
    """ Gather all the informations about the state of the installation"""
    
    def __init__(self,un_com_arduino  ):
        
        self.com_arduino = un_com_arduino
        
        """state of each pump : { P_M1_BR1 : [Lock,True] , P_M1_BR2 : [Lock, False] , ...} """
        #self.state_pumps = dict()
        self.state_pumps = { "P_M1_BR1" : [threading.Lock(),False] , "P_M1_BR2" : [threading.Lock(),False], "P_M1_BR3" : [threading.Lock(),False],\
                             "P_BR1_BU1" : [threading.Lock(),False], "P_BR2_BU2" : [threading.Lock(),False] , "P_BR3_BU3" : [threading.Lock(),False],\
                             "P_M2_BU1" : [threading.Lock(),False], "P_M2_BU2" : [threading.Lock(),False] , "P_M2_BU3" : [threading.Lock(),False], "P_M2_AQ" : [threading.Lock(),False],\
                             "P_BU1_AQ" : [threading.Lock(),False], "P_BU2_AQ" : [threading.Lock(),False] , "P_BU3_AQ" : [threading.Lock(),False],\
                             "P_AQ_S" : [threading.Lock(),False], "P_AQ_FI" : [threading.Lock(),False] , "P_FI_AQ" : [threading.Lock(),False]}
        
        """state of each electrode : { EL_M1 : True , EL_M2 : False, ...} """
        self.state_electrodes = dict()
        
        """Occupied volume for each container : { M1 : [Lock, 0.75] , M2 : ...} """
        self.occupied_volume = dict()
        
        """time of each cycle : { C1 : [Lock, 75] , C2 : ...}"""
        self.time_cycle = dict()
        
        """Number of usage for each BU : { BU1 : 0 , BU2 : 23, ...} """
        self.number_usage = dict()
        
        """BRBU_controller state"""
        self.BRBU_state = {"BU1" : [threading.Lock(), 0],"BU2" : [threading.Lock(), 0],"BU3" : [threading.Lock(), 0] }
        
        self.__setState__()
        
        self.last_time = time.time()
        
        self.image_formation = [threading.Lock(), 35]
        
        """if there is a GUI or not"""
        self.GUI = True 
    
    
    
    def P_BR1_BU1(self, state):
        name= 'P_BR1_BU1'
        self.set_state_pumps( name, state )
        
    def P_BR2_BU2(self, state):
        name= 'P_BR2_BU2'
        self.set_state_pumps( name, state )
    
    def P_BR3_BU3(self, state):
        name = 'P_BR3_BU3'
        self.set_state_pumps( name, state )
           
    def P_BU1_AQ(self, state):
        name = 'P_BU1_AQ'
        self.set_state_pumps( name, state )
                
    def P_BU2_AQ(self, state):
        name = 'P_BU2_AQ'
        self.set_state_pumps( name, state )
    
    def P_BU3_AQ(self, state):
        name = 'P_BU3_AQ'
        self.set_state_pumps( name, state )
                
    def P_M1_BR1(self, state):
        name = 'P_M1_BR1'
        self.set_state_pumps( name, state )
   
    def P_M1_BR2(self, state):
        name = 'P_M1_BR2'
        self.set_state_pumps( name, state )
                
    def P_M1_BR3(self, state):
        name = 'P_M1_BR3'
        self.set_state_pumps( name, state )
                
    def P_M2_BU1(self, state):
        name = 'P_M2_BU1'
        self.set_state_pumps( name, state )
   
    def P_M2_BU2(self, state):
        name = 'P_M2_BU2'
        self.set_state_pumps( name, state )
        
    def P_M2_BU3(self, state):
        name = 'P_M2_BU3'
        self.set_state_pumps( name, state )
                           
    def P_M2_AQ(self, state):
        name = 'P_M2_AQ'
        self.set_state_pumps( name, state )
    
    def P_AQ_S(self, state):
        name = 'P_AQ_S'
        self.set_state_pumps( name, state )
        
    def P_AQ_FI(self, state):
        name = 'P_AQ_FI'
        self.set_state_pumps( name, state )
        
    def P_FI_AQ(self, state):
        name = 'P_FI_AQ'
        self.set_state_pumps( name, state )
        
        self.refresh_windows()
        
    def get_state_pumps(self, name):
        self.state_pumps[name][0].acquire()
        state = self.state_pumps[name][1]
        self.state_pumps[name][0].release()
        return state
    
    """do not use this function from outside"""
    def _set_state_pumps(self, name, state ):
        self.state_pumps[name][0].acquire()
        self.state_pumps[name][1] = state
        self.state_pumps[name][0].release()
    """use this function to set a pump state"""
    
    def set_state_pumps(self, name, state ):
        if not self.get_state_pumps( name) == state:
            """ask com arduino to set the pump"""
            order_ok = self.com_arduino.pump_order(name,state)
            
            """if com_arduino return True, it means order has been successfully conducted""" 
            if order_ok :
                self._set_state_pumps(name, state )
            else : 
                print("fail to activate or desactivate " + name )
            
            
            self.refresh_windows()
            for item in self.occupied_volume : 
                print(item + " " + str(self.get_occupied_volume(item)))

    
    def get_occupied_volume(self, name):
        self.occupied_volume[name][0].acquire()
        v = self.occupied_volume[name][1]
        self.occupied_volume[name][0].release()
        return v
    
    def set_occupied_volume(self, name, v):
        self.occupied_volume[name][0].acquire()
        self.occupied_volume[name][1] = v
        self.occupied_volume[name][0].release()
        """refresh GUI"""
        self.refresh_windows()
  
        
        return bool
            
    def set_windows(self,window):
        self.window = window
         
    def refresh_windows(self):
        if self.GUI :
            delta = time.time() -self.last_time
            if delta > 0.01 :
                """refresh the GUI"""
                #add in the thread of Tkinter the draw function
                #self.window.after(0,self.window.refresh)
                self.window.after(0,self.window.refresh)
                #self.window.visual_feedback.after_idle(self.window.visual_feedback.draw)
                self.last_time = time.time()
        
                print("refresh") 
            
            #for item in self.state_pumps : 
                #print(self.get_state_pumps(item))
            
        
    def set_BRBU_state(self, BU, state):
        """set the state of BU"""
        self.BRBU_state[BU][0].acquire()
        self.BRBU_state[BU][1] = state
        self.BRBU_state[BU][0].release()
        
    def get_BRBU_state(self, BU):
        """set the state of BU"""
        self.BRBU_state[BU][0].acquire()
        state = self.BRBU_state[BU][1]
        self.BRBU_state[BU][0].release()
        return state
    
    def get_image_formation(self):
        """get the value of image_formation"""
        self.image_formation[0].acquire()
        value = self.image_formation[1]
        self.image_formation[0].release()
        return value
    
    def set_image_formation(self, value):
        """set the value of image_formation"""
        self.image_formation[0].acquire()
        self.image_formation[1] = value
        self.image_formation[0].release[0]
    
    def __setState__(self):
        """ Set the states to the right values according to the log_start.txt file """
            # Open the file
        log_pin = open("log_start.txt", "r")
     
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
                self.occupied_volume[list[1].strip()] = [threading.Lock(), float(list[2].strip())]
                
            elif list[0].strip() =="number_usage" :
                """set the number_usage { BU1 : 0 , BU2 : 23, ...} """
                self.number_usage[list[1].strip()] = int(list[2].strip())


    
"""
if __name__ == "__main__":
    a = current_state()
    #print(a.the_pins)
"""  
    
    
        
    
