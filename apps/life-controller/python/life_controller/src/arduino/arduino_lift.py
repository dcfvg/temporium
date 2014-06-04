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
            self.start_busy()
            answer = True
        
        
        print("end output")
        return answer

    def liftDown(self):
       
        """if busy"""
        if self.get_busy_state() : 
            print ("Arduino lift busy")
            answer = False
            """if free"""
        else : 
            
            self.lock.acquire()
            
            self.__sendData('0')
            
            self.lock.release()
            self.start_busy()
            answer = True
            
        return answer

    def liftUp(self):
        """if busy"""
        if self.get_busy_state() : 
            print ("Arduino lift busy")
            answer = False
            """if free"""
        else : 
            
            self.lock.acquire()
            self.__sendData('1')
            self.lock.release()
            self.start_busy()
            answer = True
            
        return answer

    def screenDown(self):
        """if busy"""
        if self.get_busy_state() : 
            print ("Arduino lift busy")
            answer = False
            """if free"""
        else : 
            
            self.lock.acquire()
            self.__sendData('2')
            self.lock.release()
            self.start_busy()
            answer = True
            
        return answer

    def screenUp(self):
        """if busy"""
        if self.get_busy_state() : 
            print ("Arduino lift busy")
            answer = False
            """if free"""
        else : 
            
            self.lock.acquire()
            self.__sendData('3')
            self.lock.release()
            self.start_busy()
            answer = True
            
        return answer
    
    """check if the arduino is occupied, do not use this function
    will stay in this function until the arduin is free again"""
    def _is_occupied(self):
        self.lock.acquire()
        self.__sendData('4')
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
    def start_busy(self):
        self.arduino_lift_thread.start_busy()
    
    def close(self):
        self.lock.acquire()
        self.serial.close()
        self.lock.release()
        return True