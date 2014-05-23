#!/usr/bin/env python

import serial
import threading

class arduino_lift(object):

    __OUTPUT_PINS = -1

    def __init__(self, port, baudrate=115200):
        self.serial = serial.Serial(port, baudrate)
        self.serial.write(bytearray('99','utf-8'))
        
        """to secure the access to the arduino to only one person at the same time"""
        self.lock = threading.Lock()

    def __str__(self):
        return "Arduino is on port %s at %d baudrate" %(self.serial.port, self.serial.baudrate)

    def output(self, pinArray):
        self.lock.acquire()
        
        self.__sendData(len(pinArray))

        if(isinstance(pinArray, list) or isinstance(pinArray, tuple)):
            self.__OUTPUT_PINS = pinArray
            for each_pin in pinArray:
                self.__sendData(each_pin)
        
        self.lock.release()
        return True

    def liftDown(self):
        self.lock.acquire()
        self.__sendData('0')
        self.lock.release()
        return True

    def liftUp(self):
        self.lock.acquire()
        self.__sendData('1')
        self.lock.release()
        return True

    def screenDown(self):
        self.lock.acquire()
        self.__sendData('2')
        self.lock.release()
        return True

    def screenUp(self):
        self.lock.acquire()
        self.__sendData('3')
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
    

    def close(self):
        self.lock.acquire()
        self.serial.close()
        self.lock.release()
        return True