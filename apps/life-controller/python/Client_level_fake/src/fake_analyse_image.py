'''
Created on May 6, 2014
 
@author: glogzy
'''
import threading
from client_level import *
from client_arduino_order import *
import time

 
 
 
class fake_analyse_image(threading.Thread):
    '''
    classdocs
    '''
 
 
    def __init__(self):
        '''
        Constructor
        '''
        threading.Thread.__init__ (self, target=self.run)
        """pump_flow_rate in ml/s"""
        self.pump_flow_rate = 300*(50/60)
      
         
        self._state_pumps = { "P_M1_BR1" : [threading.Lock(),False] , "P_M1_BR2" : [threading.Lock(),False], "P_M1_BR3" : [threading.Lock(),False],\
                             "P_BR1_BU1" : [threading.Lock(),False], "P_BR2_BU2" : [threading.Lock(),False] , "P_BR3_BU3" : [threading.Lock(),False],\
                             "P_M2_BU1" : [threading.Lock(),False], "P_M2_BU2" : [threading.Lock(),False] , "P_M2_BU3" : [threading.Lock(),False], "P_M2_AQ" : [threading.Lock(),False],\
                             "P_BU1_FI" : [threading.Lock(),False], "P_BU2_FI" : [threading.Lock(),False] , "P_BU3_FI" : [threading.Lock(),False],\
                             "P_AQ_S" : [threading.Lock(),False], "P_AQ_FI" : [threading.Lock(),False] , "P_FI_AQ_1" : [threading.Lock(),False], "P_FI_AQ_3" : [threading.Lock(),False],\
                             "P_FI_S" : [threading.Lock(),False]}
         
        self.initial_volume = {"M1" : 10000,"M2" : 10000, "BR1" : 5000,"BR2" : 5000,"BR3" : 5000, "BU1" : 5000, "BU2" : 5000, "BU3" : 5000, "AQ" : 8000, "S" : 10000, "FI" : 1000}
        
        self.current_time = { "P_M1_BR1" : time.time() , "P_M1_BR2" : time.time(), "P_M1_BR3" : time.time(),\
                             "P_BR1_BU1" : time.time(), "P_BR2_BU2" : time.time() , "P_BR3_BU3" : time.time(),\
                             "P_M2_BU1" : time.time(), "P_M2_BU2" : time.time() , "P_M2_BU3" : time.time(), "P_M2_AQ" : time.time(),\
                             "P_BU1_FI" : time.time(), "P_BU2_FI" : time.time() , "P_BU3_FI" : time.time(),\
                             "P_AQ_FI" : time.time(), "P_FI_AQ_1" : time.time(), "P_FI_AQ_3" : time.time(), \
                             "P_AQ_S" : time.time(), "P_FI_S" : time.time()}

         
        """Occupied volume for each container :{'M1': 3, 'M2': 2} """
        self._occupied_volume = dict()
         
        
        
        """state of the EL {"AQ" : {"HIGH" : [threading.Lock(),False,1], "MEDIUM" : [threading.Lock(),False,0.66] },... }"""
        self._state_EL = dict()
     
        """Its goal is to receive order to start and stop sending level information"""

        
        
        """Boolean : if information is asked by life_controller or not"""
        self._information_asked = [threading.Lock(),False]
         
        """ check in the log_start.txt to set occupied_volume"""
        self.__setState__()
        
        self.stop = False
         
    def run (self):
       
        while not self.stop :
            for item in self._state_pumps : 
                self.calcul_volume(item)
                    
            """send information about level to the life_controller app if asked"""
            """protocol : '{'M1': 3, 'M2': 2}' """       
            
            if self.get_information_asked() :
             
                self.send_occupied_volume()
                
            # print(self._state_pumps)
            #print(str(self.occupied_volume))
            time.sleep(0.05)

            # a completer
    def send_occupied_volume(self):
        msg = dict()
        for item in self._occupied_volume : 
            msg [item] = round(self.get_occupied_volume(item)  ,2) 
        string = str(msg)
        string = string.replace("{","")
        string = string.replace("}","")
        string = string.replace("'","")
        self.client_level._send(string)
    
    def pump_order(self, name , state):
        """set the state of the pump to 'state' """
        self._state_pumps[name] = state ; 
                 
    def __setState__(self):
            """ Set the states to the right values according to the log_start.txt file """
                # Open the file
            log_pin = open("config/config_start.txt", "r")
          
            # read the ligne one by one
            for ligne in log_pin:
                #Take out the end symbols (\n)
                ligne = ligne.strip()
                #split on  ":"
                list = ligne.split(":")
                 
                         
                if list[0].strip() =="occupied_volume" :
                    """set the occupied volume { M1 : [Lock, 0.75] , C2 : ...} """
                    self._occupied_volume[list[1].strip()] = [threading.Lock(), float(list[2].strip())]
                
                elif list[0].strip() =="EL" :
                    
                    """Make a dictionnary of the EL for a container, then put it in the_EL :  {"AQ" : {"HIGH" : [threading.Lock(),False,1], "MEDIUM" : [threading.Lock(),False,0.66] },... } """
                    """if name_container not in the dict, we create a dictionnary for it in the_EL dictionnary"""
                    name_container =list[1].strip() 
                    name_EL = list[2].strip()
                    level_ref = list[3].strip()
                    if not name_container in self._state_EL :
                        self._state_EL[name_container] = {}
                    if level_ref == "NULL" : 
                        self._state_EL[name_container][name_EL] = [threading.Lock(),False,level_ref ]
                    else: 
                        self._state_EL[name_container][name_EL] = [threading.Lock(),False,float(level_ref) ]
    
    
    def set_client_level(self,client_l ):
        """creation of the client_level""" 
        self.client_level = client_l
    
    """EL asking"""
    def ask_EL(self, name_container, name_El):
        self._state_EL[name_container][name_El][0].acquire()
        
        if self.get_occupied_volume(name_container) >= self._state_EL[name_container][name_El][2] : 
            state = True
            self._state_EL[name_container][name_El][1] = True
        else  : 
            state = False
            self._state_EL[name_container][name_El][1] = False
        self._state_EL[name_container][name_El][0].release()
        
        return state
            
    def get_occupied_volume(self, name):
        self._occupied_volume[name][0].acquire()
        v = self._occupied_volume[name][1]
        self._occupied_volume[name][0].release()
        return v
    
    def set_occupied_volume(self, name, v):
        """no need to have more precision"""
        self._occupied_volume[name][0].acquire()
        self._occupied_volume[name][1] = v
        self._occupied_volume[name][0].release()
    
    def calcul_volume(self, name):   
        if self.get_state_pump(name) :
            name_list = name.split("_")
            Container_from = name_list[1]
            Container_to = name_list[2]
            memory_currrent_time = time.time()
            interval_time_used = memory_currrent_time - self.current_time[name]
            self.current_time[name] = memory_currrent_time
            new_volume_from = (self.get_occupied_volume(Container_from)*self.initial_volume[Container_from] - interval_time_used*self.pump_flow_rate)/self.initial_volume[Container_from]
            new_volume_to = (self.get_occupied_volume(Container_to)*self.initial_volume[Container_to] + interval_time_used*self.pump_flow_rate)/self.initial_volume[Container_to]
            self.set_occupied_volume(Container_from,new_volume_from) 
            self.set_occupied_volume(Container_to,new_volume_to) 
        else :
            self.current_time[name] = time.time()
    
        #"""asking for connection"""
        #self.client_level.ask_connection('localhost', 8000)
    
    def get_state_pump(self, name):
        self._state_pumps[name][0].acquire()
        state = self._state_pumps[name][1]
        self._state_pumps[name][0].release()
        return state
    
    def set_state_pump(self, name, state ):
        self._state_pumps[name][0].acquire()
        self._state_pumps[name][1] = state
        self._state_pumps[name][0].release()
    
    def get_information_asked(self):
        self._information_asked[0].acquire()
        state = self._information_asked[1]
        self._information_asked[0].release()
        return state
    
    def set_information_asked(self, state):
        self._information_asked[0].acquire()
        self._information_asked[1] = state 
        self._information_asked[0].release()
    
         
    
    
     
    #print(a.the_pins)