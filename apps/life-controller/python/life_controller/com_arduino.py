from arduino import*
import time 
'''
Created on Apr 21, 2014

@author: Cactus
'''

class com_arduino(object):
    '''
    Control the Arduino-microcontroller
    Set he pins input/output from a log_arduino.txt file at the begining.  
    '''


    def __init__(self):
        '''
        Constructor
     
        '''
        #dictionnaire des pins {"P_M1_BR1" : [arduino_current,pin], "P_M2_BU2" : [arduino_current,pin], ...}
        self.the_pins = dict()
        #dictionnaire des arduino {"arduino_une" : arduino_uno, ...}
        self.the_arduino = dict()
        #pin_array for arduino {arduino_current : [pin, pin, ...], ...}
        self.pin_array = dict()
        
        self.test = True
       
        self.__setPin__()
        
        
        
        
    """Pump order"""   
    def P_BR1_BU1(self, state):
        name = 'P_BR1_BU1'
        if not self.test : 
            if self.the_pins[name][1]=="NULL" :
                print("pin not connected")
            else : 
                if state : 
                    self.the_pins[name][0].setHigh(self.the_pins[name][1])
                    print(name + " HIGH")
                else : 
                    self.the_pins[name][0].setLow(self.the_pins[name][1])
               
        if state : 
            print(name + " HIGH")
        else : 
            print(name + " LOW")
            
        return True
                
        
   
    def P_BR2_BU2(self, state):
        name = 'P_BR2_BU2'
        if not self.test : 
            if self.the_pins[name][1]=="NULL" :
                print("pin not connected")
            else : 
                if state : 
                    self.the_pins[name][0].setHigh(self.the_pins[name][1])
                    print(name + " HIGH")
                else : 
                    self.the_pins[name][0].setLow(self.the_pins[name][1])
               
        if state : 
            print(name + " HIGH")
        else : 
            print(name + " LOW")
            
        return True

        
        
    def P_BR3_BU3(self, state):
        name = 'P_BR3_BU3'
        if not self.test : 
            if self.the_pins[name][1]=="NULL" :
                print("pin not connected")
            else : 
                if state : 
                    self.the_pins[name][0].setHigh(self.the_pins[name][1])
                    print(name + " HIGH")
                else : 
                    self.the_pins[name][0].setLow(self.the_pins[name][1])
               
        if state : 
            print(name + " HIGH")
        else : 
            print(name + " LOW")
        
        return True
           
    def P_BU1_AQ(self, state):
        name = 'P_BU1_AQ'
        if not self.test : 
            if self.the_pins[name][1]=="NULL" :
                print("pin not connected")
            else : 
                if state : 
                    self.the_pins[name][0].setHigh(self.the_pins[name][1])
                    print(name + " HIGH")
                else : 
                    self.the_pins[name][0].setLow(self.the_pins[name][1])
               
        if state : 
            print(name + " HIGH")
        else : 
            print(name + " LOW")
        
        return True
                
    def P_BU2_AQ(self, state):
        name = 'P_BU2_AQ'
        if not self.test : 
            if self.the_pins[name][1]=="NULL" :
                print("pin not connected")
            else : 
                if state : 
                    self.the_pins[name][0].setHigh(self.the_pins[name][1])
                    print(name + " HIGH")
                else : 
                    self.the_pins[name][0].setLow(self.the_pins[name][1])
               
        if state : 
            print(name + " HIGH")
        else : 
            print(name + " LOW")
        
        return True
    
    def P_BU3_AQ(self, state):
        name = 'P_BU3_AQ'
        if not self.test : 
            if self.the_pins[name][1]=="NULL" :
                print("pin not connected")
            else : 
                if state : 
                    self.the_pins[name][0].setHigh(self.the_pins[name][1])
                    print(name + " HIGH")
                else : 
                    self.the_pins[name][0].setLow(self.the_pins[name][1])
               
        if state : 
            print(name + " HIGH")
        else : 
            print(name + " LOW")
        
        return True
                
    def P_M1_BR1(self, state):
        name = 'P_M1_BR1'
        if not self.test : 
            if self.the_pins[name][1]=="NULL" :
                print("pin not connected")
            else : 
                if state : 
                    self.the_pins[name][0].setHigh(self.the_pins[name][1])
                    print(name + " HIGH")
                else : 
                    self.the_pins[name][0].setLow(self.the_pins[name][1])
               
        if state : 
            print(name + " HIGH")
        else : 
            print(name + " LOW")
        
        return True
   
    def P_M1_BR2(self, state):
        name = 'P_M1_BR2'
        if not self.test : 
            if self.the_pins[name][1]=="NULL" :
                print("pin not connected")
            else : 
                if state : 
                    self.the_pins[name][0].setHigh(self.the_pins[name][1])
                    print(name + " HIGH")
                else : 
                    self.the_pins[name][0].setLow(self.the_pins[name][1])
               
        if state : 
            print(name + " HIGH")
        else : 
            print(name + " LOW")
        
        return True
                
    def P_M1_BR3(self, state):
        name = 'P_M1_BR3'
        if not self.test : 
            if self.the_pins[name][1]=="NULL" :
                print("pin not connected")
            else : 
                if state : 
                    self.the_pins[name][0].setHigh(self.the_pins[name][1])
                    print(name + " HIGH")
                else : 
                    self.the_pins[name][0].setLow(self.the_pins[name][1])
               
        if state : 
            print(name + " HIGH")
        else : 
            print(name + " LOW")
        
        return True
                
    def P_M2_BU1(self, state):
        name = 'P_M2_BU1'
        if not self.test : 
            if self.the_pins[name][1]=="NULL" :
                print("pin not connected")
            else : 
                if state : 
                    self.the_pins[name][0].setHigh(self.the_pins[name][1])
                    print(name + " HIGH")
                else : 
                    self.the_pins[name][0].setLow(self.the_pins[name][1])
               
        if state : 
            print(name + " HIGH")
        else : 
            print(name + " LOW")
        
        return True
   
    def P_M2_BU2(self, state):
        name = 'P_M2_BU2'
        if not self.test : 
            if self.the_pins[name][1]=="NULL" :
                print("pin not connected")
            else : 
                if state : 
                    self.the_pins[name][0].setHigh(self.the_pins[name][1])
                    print(name + " HIGH")
                else : 
                    self.the_pins[name][0].setLow(self.the_pins[name][1])
               
        if state : 
            print(name + " HIGH")
        else : 
            print(name + " LOW")
            
        return True
    
    def P_M2_BU3(self, state):
        name = 'P_M2_BU3'
        if not self.test : 
            if self.the_pins[name][1]=="NULL" :
                print("pin not connected")
            else : 
                if state : 
                    self.the_pins[name][0].setHigh(self.the_pins[name][1])
                    print(name + " HIGH")
                else : 
                    self.the_pins[name][0].setLow(self.the_pins[name][1])
               
        if state : 
            print(name + " HIGH")
        else : 
            print(name + " LOW")
        
        return True
                           
    def P_M2_AQ(self, state):
        name = 'P_M2_AQ'
        if not self.test : 
            if self.the_pins[name][1]=="NULL" :
                print("pin not connected")
            else : 
                if state : 
                    self.the_pins[name][0].setHigh(self.the_pins[name][1])
                    print(name + " HIGH")
                else : 
                    self.the_pins[name][0].setLow(self.the_pins[name][1])
               
        if state : 
            print(name + " HIGH")
        else : 
            print(name + " LOW")
        
        return True
    
    def P_AQ_S(self, state):
        name = 'P_AQ_S'
        if not self.test : 
            if self.the_pins[name][1]=="NULL" :
                print("pin not connected")
            else : 
                if state : 
                    self.the_pins[name][0].setHigh(self.the_pins[name][1])
                    print(name + " HIGH")
                else : 
                    self.the_pins[name][0].setLow(self.the_pins[name][1])
               
        if state : 
            print(name + " HIGH")
        else : 
            print(name + " LOW")
        
        return True
    
    def pump_order(self, name , state):
        
        if not self.test : 
            if self.the_pins[name][1]=="NULL" :
                print("pin not connected")
            else : 
                if state : 
                    self.the_pins[name][0].setHigh(self.the_pins[name][1])
                    print(name + " HIGH")
                else : 
                    self.the_pins[name][0].setLow(self.the_pins[name][1])
               
        if state : 
            print(name + " HIGH")
        else : 
            print(name + " LOW")
        
        return True
    
    
    #Read analog Input
    def EL_BR1(self):
        """Return the value of the EL_BR1, return -1 if not connected to the arduino"""
        name = "EL_BR1"
        if self.the_pins[name][1]=="NULL" :
            print("pin not connected")
            return -1
        else :
            if not self.test  :
                return self.the_pins[name][0].analogRead(self.the_pins[name][1])               
            
    def __setPin__(self):
        """if not in test mode (without arduino connected)"""
        if not self.test  :
            """ Set the pin to the right function according to the log_pin.txt file """
            # Open the file
            log_pin = open("log_pin.txt", "r")
     
            # read the ligne one by one
            for ligne in log_pin:
                #Take out the end symbols (\n)
                ligne = ligne.strip()
                #split on  ":" 
                list = ligne.split(":")
                
                
                
                if list[0].strip() == "comments" :
                    print (list[1].strip())
                
                elif list[0].strip() == "arduino" : 
                    """Make an arduino with the port from the log_pin.txt file, and put it in the dict() the_arduino
                    arduino_current to associate the pin to the right arduino (the last built arduino )"""
                    self.the_arduino[list[1].strip()] = Arduino(list[2].strip())
                    arduino_current = self.the_arduino[list[1].strip()]
                    print (list[1].strip() +" made on port :" + list[2].strip())
                    
                    
                elif list[0].strip() =="pin_array" :
                    """Make a dictionnary of the pin_array : {arduino_current : [pin, pin, ...], ...} """
                    list_pin = list[1].strip().split(",")
                    self.pin_array[arduino_current] = []
                    for item in list_pin :
                        self.pin_array[arduino_current].append(int (item.strip()))
                    
                else : 
                    """put the pin into the the_pins dict() : {P_M1_BR1 : [arduino_current,pin], P_M2_BU2 : [arduino_current,pin], ...}"""
                    if list[1].strip()=="NULL" :
                        self.the_pins[list[0].strip()] = [arduino_current,list[1].strip()]
                    else : 
                        self.the_pins[list[0].strip()] = [arduino_current,int(list[1].strip())]
                        
            """def output Arduino"""
            
            for ard in self.pin_array : 
                print(self.pin_array[ard])
                ard.output(self.pin_array[ard])
            
        
        
            
         
                
"""
if __name__ == "__main__":
    a = com_arduino()
    #print(a.the_pins)
    while True : 
        a.P_M2_BU1(True)
        time.sleep(2)
        a.P_M2_BU1(False)
        time.sleep(2)
"""
    
    
    
 
            
             
        
        