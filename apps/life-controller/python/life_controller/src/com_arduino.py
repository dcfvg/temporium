from arduino.arduino_mega import*
from arduino.arduino_lift import *
import time
'''
Created on Apr 21, 2014
 
@author: Cactus
'''
import threading


"""things to do  : 
    - protect access to each arduino by a mutex, only one thread can access to one arduino at the same time !
    - server fake arduino : answer to EL information request """
 
class com_arduino(object):
    '''
    Control the Arduino-microcontroller
    Set he pins input/output from a log_arduino.txt file at the begining. 
    '''
 
 
    def __init__(self, test):
        '''
        Constructor
      
        '''
        #dictionnaire des pins {"P_M1_BR1" : [arduino_current,pin], "P_M2_BU2" : [arduino_current,pin], ...}
        self.the_pumps = dict()
        #dictionnaire des arduino {"arduino_mega" : arduino_mega, "arduino_lift" : arduino_lift ...}
        self.the_arduino = dict()
        #pin_array_output for arduino {arduino_current : [pin, pin, ...], ...}
        self.pin_array_output = dict()
        
        """{"AQ" : {"HIGH" : [arduino, pin, pin_5V],"MEDIUM" : [arduino, pin, , pin_5V], "LOW" : [arduino, pin, , pin_5V] }, "BR1" :  {"HIGH" : [arduino, pin, pin_5V],"MEDIUM" : [arduino, pin, pin_5V], "LOW" : [arduino, pin, pin_5V] }}"""
        self.the_EL = dict()
        
        """pin for the spectro : {"SPECTRO = [arduino, pin])"""
        self.the_SPECTRO = dict()
         
        """for simulation and testing"""
         
        """do not try to connect with Arduino"""
        self.test = test
         
        """send order received to the client connected"""
        self.server_arduino_order_state = [threading.Lock() , False]
         
         
         
    """Pump order"""  
    def P_BR1_BU1(self, state):
        name = 'P_BR1_BU1'
        self.pump_order(name, state)
                 
    def P_BR2_BU2(self, state):
        name = 'P_BR2_BU2'
        self.pump_order(name, state)
            
    def P_BR3_BU3(self, state):
        name = 'P_BR3_BU3'
        self.pump_order(name, state)
            
    def P_BU1_FI(self, state):
        name = 'P_BU1_FI'
        self.pump_order(name, state)
                 
    def P_BU2_FI(self, state):
        name = 'P_BU2_FI'
        self.pump_order(name, state)
     
    def P_BU3_FI(self, state):
        name = 'P_BU3_FI'
        self.pump_order(name, state)
                 
    def P_M1_BR1(self, state):
        name = 'P_M1_BR1'
        self.pump_order(name, state) 
    
    def P_M1_BR2(self, state):
        name = 'P_M1_BR2'
        self.pump_order(name, state)
                 
    def P_M1_BR3(self, state):
        name = 'P_M1_BR3'
        self.pump_order(name, state)
                 
    def P_M2_BU1(self, state):
        name = 'P_M2_BU1'
        self.pump_order(name, state)
    
    def P_M2_BU2(self, state):
        name = 'P_M2_BU2'
        self.pump_order(name, state)
     
    def P_M2_BU3(self, state):
        name = 'P_M2_BU3'
        self.pump_order(name, state)
                            
    def P_M2_AQ(self, state):
        name = 'P_M2_AQ'
        self.pump_order(name, state)
     
    def P_AQ_S(self, state):
        name = 'P_AQ_S'
        self.pump_order(name, state)        
    
    def P_AQ_FI(self, state):
        name = 'P_AQ_FI'
        self.pump_order(name, state)     
        
    def P_FI_AQ_1(self, state):
        """control 1 pump from FI to AQ"""
        name = 'P_FI_AQ_1'
        self.pump_order(name, state)
    
    def P_FI_AQ_3(self, state):
        """control 3 pump from FI to AQ"""
        name = 'P_FI_AQ_3'
        self.pump_order(name, state)
        
    def P_FI_S(self, state):
        """control 3 pump from FI to AQ"""
        name = 'P_FI_S'
        self.pump_order(name, state)
    
    def P_SPECTRO(self, state):
        """control 3 pump from FI to AQ"""
        name = 'P_SPECTRO'
        self.pump_order(name, state)
        
    def pump_order(self, name , state):
        
        """if not in test mode"""
        if not self.test :
            """if arduino_pimp connected"""
            if "arduino_pump" in self.the_arduino :  
                if self.the_pumps[name][1]=="NULL" :
                    print("pin not connected")
                else :
                    if state :
                        self.the_pumps[name][0].setHigh(self.the_pumps[name][1])
                    else :
                        self.the_pumps[name][0].setLow(self.the_pumps[name][1])      
            else : 
                print ("arduino_pump not declared/connected")
        """send information to arduino_server"""
        self.send_server_arduino_order("PUMP", name, state)
        if state :
            print(name + " HIGH") 
        else :
            print(name + " LOW")
                
        return True 
    
    
    """order to turn on/off the spectro_light"""
    def spectro_light(self, state):
        name = "SPECTRO_LIGHT"
        """if not in test mode"""
        if not self.test :
            """if arduino_pump connected"""
            if "arduino_pump" in self.the_arduino :  
                if self.the_SPECTRO[name][1]=="NULL" :
                    print("pin not connected")
                else :
                    if state :
                        self.the_SPECTRO[name][0].setHigh(self.the_SPECTRO[name][1])
                    else :
                        self.the_SPECTRO[name][0].setLow(self.the_SPECTRO[name][1])      
            else : 
                print ("arduino_pump not declared/connected")
        """send information to arduino_server"""
        self.send_server_arduino_order("LIGHT", name, state)
        if state :
            print(name + " HIGH") 
        else :
            print(name + " LOW")
                
        return True 
        
    
    """order to read EL"""
    
    """Return the value of the EL_BR1, return "NULL" if not connected to the arduino"""
    def EL_read(self,name_container, name_EL):
        if not self.test :
            if "arduino_EL" in self.the_arduino : 
                if self.the_EL[name_container][name_EL][1] == "NULL":
                    print("pin not connected")
                    return "NULL"
                else : 
                    if not self.test  :
                        """set the pin_5V to high"""
                        self.the_EL[name_container][name_EL][0].setHigh(self.the_EL[name_container][name_EL][2]) 
                        
                        """check the EL"""
                        value = self.the_EL[name_container][name_EL][0].getState(self.the_EL[name_container][name_EL][1])
                        
                        """set the pin_5V to low"""
                        self.the_EL[name_container][name_EL][0].setLow(self.the_EL[name_container][name_EL][2])           
                        
                        """boolean"""
                        return value
            else : 
                print ("arduino_EL not declared/connected")
                 
        else : 
            return self.ask_server_arduino_EL(name_container,name_EL)
        
            #return False
     
    """Automatic Order to liftDown and liftUp, screenDown and screenUp"""
    def lift_down(self):
        """answer : True if order send to the arduino, false otherwise"""
        answer = False
        if not self.test : 
            if "arduino_lift" in self.the_arduino : 
                """send the order to liftdown the lift"""
                answer = self.the_arduino["arduino_lift"].lift_down()
            else : 
                print ("arduino_lift not declared/connected")   
        
        print("LiftDown asked")
            
        return answer

    def lift_up(self):
        """answer : True if order send to the arduino, false otherwise"""
        answer = False
        if not self.test : 
            if "arduino_lift" in self.the_arduino :
                """send the order to liftUp the lift"""
                answer = self.the_arduino["arduino_lift"].lift_up()
            else : 
                print ("arduino_lift not declared/connected")      
        print("LiftUp asked")
        
        return answer

    def screen_down_outside(self):
        """answer : True if order send to the arduino, false otherwise"""
        answer = False
        if not self.test : 
            if "arduino_lift" in self.the_arduino :
                """send the order to screenDown"""
                answer = self.the_arduino["arduino_lift"].screen_down_outside()
            else : 
                print ("arduino_lift not declared/connected")
        print("screenDown asked")
        return answer 

    def screen_up_outside(self):
        """answer : True if order send to the arduino, false otherwise"""
        answer = False
        if not self.test : 
            if "arduino_lift" in self.the_arduino :
                """send the order to screenDown"""
                answer = self.the_arduino["arduino_lift"].screen_up_outside()
            else : 
                print ("arduino_lift not declared/connected")  
        print("screenUp asked")
        
        return answer
    
    def screen_down_inside(self):
        """answer : True if order send to the arduino, false otherwise"""
        answer = False
        if not self.test : 
            if "arduino_lift" in self.the_arduino :
                """send the order to screenDown"""
                answer = self.the_arduino["arduino_lift"].screen_down_inside()
            else : 
                print ("arduino_lift not declared/connected")
        print("screenDown asked")
        return answer 

    def screen_up_inside(self):
        """answer : True if order send to the arduino, false otherwise"""
        answer = False
        if not self.test : 
            if "arduino_lift" in self.the_arduino :
                """send the order to screenDown"""
                answer = self.the_arduino["arduino_lift"].screen_up_inside()
            else : 
                print ("arduino_lift not declared/connected")  
        print("screenUp asked")
        
        return answer
    
    """Manual Order to liftDown and liftUp, screenDown and screenUp"""
    def lift_down_manual(self):
        """answer : True if order send to the arduino, false otherwise"""
        answer = False
        if not self.test : 
            if "arduino_lift" in self.the_arduino : 
                """send the order to liftdown manually the lift"""
                answer = self.the_arduino["arduino_lift"].lift_down_manual()
            else : 
                print ("arduino_lift not declared/connected")   
        
        print("LiftDown Manual asked")
            
        return answer

    def lift_up_manual(self):
        """answer : True if order send to the arduino, false otherwise"""
        answer = False
        if not self.test : 
            if "arduino_lift" in self.the_arduino :
                """send the order to liftUp manually the lift"""
                answer = self.the_arduino["arduino_lift"].lift_up_manual()
            else : 
                print ("arduino_lift not declared/connected")      
        print("LiftUp Manual asked")
        
        return answer

    def screen_down_outside_manual(self):
        """answer : True if order send to the arduino, false otherwise"""
        answer = False
        if not self.test : 
            if "arduino_lift" in self.the_arduino :
                """send the order to screenDown manually"""
                answer = self.the_arduino["arduino_lift"].screen_down_outside_manual()
            else : 
                print ("arduino_lift not declared/connected")
        print("screenDown Manual asked")
        return answer 

    def screen_up_outside_manual(self):
        """answer : True if order send to the arduino, false otherwise"""
        answer = False
        if not self.test : 
            if "arduino_lift" in self.the_arduino :
                """send the order to screenDown manually"""
                answer = self.the_arduino["arduino_lift"].screen_up_outside_manual()
            else : 
                print ("arduino_lift not declared/connected")  
        print("screenUp Manual asked")
        
        return answer
    
    def screen_down_inside_manual(self):
        """answer : True if order send to the arduino, false otherwise"""
        answer = False
        if not self.test : 
            if "arduino_lift" in self.the_arduino :
                """send the order to screenDown manually"""
                answer = self.the_arduino["arduino_lift"].screen_down_inside_manual()
            else : 
                print ("arduino_lift not declared/connected")
        print("screenDown Manual asked")
        return answer 

    def screen_up_inside_manual(self):
        """answer : True if order send to the arduino, false otherwise"""
        answer = False
        if not self.test : 
            if "arduino_lift" in self.the_arduino :
                """send the order to screenDown manually"""
                answer = self.the_arduino["arduino_lift"].screen_up_inside_manual()
            else : 
                print ("arduino_lift not declared/connected")  
        print("screenUp Manual asked")
        
        return answer

    """send information about order to arduino_client, like pump, spectro"""
    def send_server_arduino_order(self, type, name, state) : 
        
        self.server_arduino_order_state[0].acquire()
        
        if self.server_arduino_order_state[1] : 
            if state : 
                self.server_arduino_order._send(type + " : " + name + " : HIGH" )
            else : 
                self.server_arduino_order._send(type + " : " + name + " : LOW")
        
        self.server_arduino_order_state[0].release()  
        
    
    def ask_server_arduino_EL(self, name_container, name_EL):
        #print("information EL asked to arduin_order")
        self.server_arduino_order_state[0].acquire()
        answer = "NULL"
        
        if self.server_arduino_order_state[1] :  
            
                self.server_arduino_order._send("EL : " + name_container+ " : "  + name_EL)
                
                answer = self.server_arduino_order._answer_EL(name_container, name_EL)
        self.server_arduino_order_state[0].release()
        
        #print("answer : " + str(answer))
        return answer
        
        
        
    """set curernt_state as attribut here"""
    def set_current_state(self, cu_state):
        self.current_state = cu_state  
            
    def __readPin__(self):
        """if not in test mode (without arduino connected)"""
        if not self.test  :
            """ Set the pin to the right function according to the log_pin.txt file """
            # Open the file
            log_pin = open("config/config_pin.txt", "r")
      
            # read the ligne one by one
            for ligne in log_pin:
                #Take out the end symbols (\n)
                ligne = ligne.strip()
                #split on  ":"
                list = ligne.split(":")
                 
                 
                 
                if list[0].strip() == "comments" :
                    continue
                
                elif list[0].strip() == "print" :
                    print (list[1].strip())
                    
                elif list[0].strip() == "arduino" :
                    """Make an arduino with the port from the log_pin.txt file, and put it in the dict() the_arduino
                    arduino_current to associate the pin to the right arduino (the last built arduino )"""
                    if  list[1].strip() == "arduino_pump" :
                        self.the_arduino[list[1].strip()] = arduino_mega(list[2].strip(), self)
                        arduino_current = self.the_arduino[list[1].strip()]
                        print (list[1].strip() +" made on port :" + list[2].strip())
                    elif  list[1].strip() == "arduino_lift" : 
                        self.the_arduino[list[1].strip()] = arduino_lift(list[2].strip(), self)
                        arduino_current = self.the_arduino[list[1].strip()]
                    
                    elif  list[1].strip() == "arduino_EL" :
                        self.the_arduino[list[1].strip()] = arduino_mega(list[2].strip(), self)
                        arduino_current = self.the_arduino[list[1].strip()]
                        print (list[1].strip() +" made on port :" + list[2].strip())
                    
                    else : 
                        print("/!\ Wrong name of Arduino : " + list[1].strip() )
                                    
                                       
                     
                elif list[0].strip() =="pin_array_output" :
                    """Make a dictionnary of the pin_array_output : {arduino_current : [pin, pin, ...], ...} """
                    list_pin = list[1].strip().split(",")
                    self.pin_array_output[arduino_current] = []
                    for item in list_pin :
                        self.pin_array_output[arduino_current].append(int (item.strip()))
                
                elif list[0].strip() =="EL" :
                    
                    """Make a dictionnary of the EL for a container, then put it in the_EL : {"AQ" : {"HIGH" : [arduino, pin],"MEDIUM" : [arduino, pin], "LOW" : [arduino, pin] }, "BR1" :  {"HIGH" : [arduino, pin],"MEDIUM" : [arduino, pin], "LOW" : [arduino, pin] }} """
                    """if name_container not in the dict, we create a dictionnary for it in the_EL dictionnary"""
                    if not list[1].strip() in self.the_EL : 
                        self.the_EL[list[1].strip()] = {}
                    
                    if list[3].strip() == "NULL" : 
                        self.the_EL[list[1].strip()][list[2].strip()] = [arduino_current,list[3].strip(), list[4].strip()]
                    else : 
                        self.the_EL[list[1].strip()][list[2].strip()] = [arduino_current,int(list[3].strip()), list[4].strip()]
                
                elif list[0].strip() =="PUMP" :
                    
                    """put the pin into the the_pumps dict() : {P_M1_BR1 : [arduino_current,pin], P_M2_BU2 : [arduino_current,pin], ...}"""
                    if list[2].strip()=="NULL" :
                        self.the_pumps[list[1].strip()] = [arduino_current,list[2].strip()]
                    else :
                        self.the_pumps[list[1].strip()] = [arduino_current,int(list[2].strip())]
                
                elif list[0].strip() =="SPECTRO" :
                    """put the pin into the the_pumps dict() : {P_M1_BR1 : [arduino_current,pin], P_M2_BU2 : [arduino_current,pin], ...}"""
                    if list[2].strip()=="NULL" :
                        self.the_SPECTRO[list[1].strip()] = [arduino_current,list[2].strip()]
                    else :
                        self.the_SPECTRO[list[1].strip()] = [arduino_current,int(list[2].strip())]
                    
                
                else :
                    print( "unknown type" + ligne)
                         
            """def output Arduino"""
             
            for ard in self.pin_array_output :
                print(self.pin_array_output[ard])
                ard.output(self.pin_array_output[ard])
    
    """set the state of the serv_arduino_order"""  
    def set_server_arduino_order_state(self, state):
        self.server_arduino_order_state[0].acquire()
        self.server_arduino_order_state[1] = state
        self.server_arduino_order_state[0].release()
    
    
       
    def set_server_arduino_order(self, server_arduino_order):
        """set the server_arduino_order"""
        self.server_arduino_order = server_arduino_order
        
         
         
         
             
          
