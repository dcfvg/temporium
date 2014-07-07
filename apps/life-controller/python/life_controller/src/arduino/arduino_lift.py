#!/usr/bin/env python

import serial
import threading
from arduino.arduino_lift_thread import *

class arduino_lift(object):

    __OUTPUT_PINS = -1

    def __init__(self, port, a_com_arduino, baudrate=115200):
        self.serial = serial.Serial(port, baudrate)
        self.serial.write(bytearray('99','utf-8'))
        self.com_arduino = a_com_arduino
        
        """to secure the access to the arduino to only one person at the same time"""
        self.lock = threading.Lock()
        
        self._busy_state = [threading.Lock(), False]
        
        """thread that will set automatically busy to true or false"""  
        self.arduino_lift_thread = arduino_lift_thread(self)

    def __str__(self):
        return "Arduino is on port %s at %d baudrate" %(self.serial.port, self.serial.baudrate)

    def output(self, pinArray):
        
        """if busy"""
        if self.get_busy_state() : 
            print ("Arduino lift busy")
            answer = False
            """if free"""
        else : 
            
            self.lock.acquire()
            self.__sendData(len(pinArray))
            
            if(isinstance(pinArray, list) or isinstance(pinArray, tuple)):
                self.__OUTPUT_PINS = pinArray
                for each_pin in pinArray:
                    self.__sendData(each_pin)
            """function to lauch to set the arduino to busy of arduino"""
            self.lock.release()
            answer = True
        
        
        print("end output")
        return answer
    
    """"Automatic action on lift/screen"""
    def lift_down(self):
       
        """if busy"""
        if self.get_busy_state() : 
            print ("Arduino lift busy")
            answer = False
            """if free"""
        else : 
            
            self.lock.acquire()
            
            self.__sendData('0')
            
            self.lock.release()
            self.start_busy("lift_down")
            answer = True
            
        return answer

    def lift_up(self):
        """if busy"""
        if self.get_busy_state() : 
            print ("Arduino lift busy")
            answer = False
            """if free"""
        else : 
            
            self.lock.acquire()
            self.__sendData('1')
            self.lock.release()
            self.start_busy("lift_up")
            answer = True
            
        return answer

    def screen_down_outside(self):
        """if busy"""
        if self.get_busy_state() : 
            print ("Arduino lift busy")
            answer = False
            """if free"""
        else : 
            
            self.lock.acquire()
            self.__sendData('4')
            self.lock.release()
            self.start_busy("screen_down_outside")
            answer = True
            
        return answer

    def screen_up_outside(self):
        """if busy"""
        if self.get_busy_state() : 
            print ("Arduino lift busy")
            answer = False
            """if free"""
        else : 
            
            self.lock.acquire()
            self.__sendData('5')
            self.lock.release()
            self.start_busy("screen_up_outside")
            answer = True
            
        return answer
    
    def screen_down_inside(self):
        """if busy"""
        if self.get_busy_state() : 
            print ("Arduino lift busy")
            answer = False
            """if free"""
        else : 
            
            self.lock.acquire()
            self.__sendData('2')
            self.lock.release()
            self.start_busy("screen_down_inside")
            answer = True
            
        return answer

    def screen_up_inside(self):
        """if busy"""
        if self.get_busy_state() : 
            print ("Arduino lift busy")
            answer = False
            """if free"""
        else : 
            
            self.lock.acquire()
            self.__sendData('3')
            self.lock.release()
            self.start_busy("screen_up_inside")
            answer = True
            
        return answer
    
    """Manual Action with lift/screen"""
    def lift_down_manual(self):
       
        """if busy"""
        if self.get_busy_state() : 
            print ("Arduino lift busy")
            answer = False
            """if free"""
        else : 
            
            self.lock.acquire()
            
            self.__sendData('6')
            
            self.lock.release()
            self.start_busy("lift_down_manual")
            answer = True
            
        return answer

    def lift_up_manual(self):
        """if busy"""
        if self.get_busy_state() : 
            print ("Arduino lift busy")
            answer = False
            """if free"""
        else : 
            
            self.lock.acquire()
            self.__sendData('7')
            self.lock.release()
            self.start_busy("lift_up_manual")
            answer = True
            
        return answer
    
    def screen_down_outside_manual(self):
        """if busy"""
        if self.get_busy_state() : 
            print ("Arduino lift busy")
            answer = False
            """if free"""
        else : 
            
            self.lock.acquire()
            self.__sendData('10')
            self.lock.release()
            self.start_busy("screen_down_outside_manual")
            answer = True
            
        return answer

    def screen_up_outside_manual(self):
        """if busy"""
        if self.get_busy_state() : 
            print ("Arduino lift busy")
            answer = False
            """if free"""
        else : 
            
            self.lock.acquire()
            self.__sendData('11')
            self.lock.release()
            self.start_busy("screen_up_outside_manual")
            answer = True
            
        return answer
    
    def screen_down_inside_manual(self):
        """if busy"""
        if self.get_busy_state() : 
            print ("Arduino lift busy")
            answer = False
            """if free"""
        else : 
            
            self.lock.acquire()
            self.__sendData('8')
            self.lock.release()
            self.start_busy("screen_down_inside_manual")
            answer = True
            
        return answer

    def screen_up_inside_manual(self):
        """if busy"""
        if self.get_busy_state() : 
            print ("Arduino lift busy")
            answer = False
            """if free"""
        else : 
            
            self.lock.acquire()
            self.__sendData('9')
            self.lock.release()
            self.start_busy("screen_up_inside_manual")
            answer = True
            
        return answer

    """check if the arduino is occupied, do not use this function
    will stay in this function until the arduin is free again"""
    def _is_occupied(self):
        self.lock.acquire()
        self.__sendData('12')
        self.lock.release()
        return True

    def __sendData(self, serial_data):
        while(self.__getData()[0] != "w"):
            pass
        self.serial.write(bytearray(str(serial_data),"utf-8"))

    def __getData(self):
        return self.serial.readline().strip().decode("utf-8")

    def __formatPinState(self, pinValue):
        if pinValue == '1':
            return True
        else:
            return False
    
    """set safely the busy_state"""
    def set_busy_state(self, state):
        self._busy_state[0].acquire()
        self._busy_state[1] = state
        self._busy_state[0].release()
        
    """get safely the busy_state"""
    def get_busy_state(self):
        self._busy_state[0].acquire()
        state = self._busy_state[1]
        self._busy_state[0].release()
        return state
    
    
    """function to lauch to set the arduino to busy of arduino"""
    def start_busy(self, action_name):
        self.arduino_lift_thread.start_busy(action_name)
    
    def close(self):
        self.lock.acquire()
        self.serial.close()
        self.lock.release()
        return True