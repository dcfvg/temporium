'''
Created on 10 mai 2014

@author: ensadlab
'''
from pythonosc import osc_message_builder
from pythonosc import udp_client
from client_OSC_seance import *
from server_OSC_seance import *
from com_arduino import *
from current_state import *
import argparse
import random
import time
import threading
import os

class seance_controller(threading.Thread):
    '''
    handle the order and action to do for the film projection"""
    '''

    
    def __init__(self, un_current_state):
        
        threading.Thread.__init__(self)
        
        self.current_state = un_current_state
       
        
       
        
        """end received"""
        self.end_received = [threading.Lock(), False]
        
        """at the beginning : 
        - create client, create server
        """
        self._create_client("localhost", 3333)
        self._create_server("localhost", 3334)
        
        self._send_image_formation_state = [threading.Lock(), False]
        
        
    def film_begin(self):
        print("film time begin in 10 sec")
        time.sleep(10)
        
        """send seance begin"""
        self.client.send_seance_begin()
        
        print("starting exposure")
        os.system("bash ~/temporium/apps/capture/capture.sh")
        
        self.start()
        compt = 0 
        
        
        """while film not end or timeout = 40 min """
        self.set_end_film(False)
        
        while not self.get_end_received() or compt > 1200:
            time.sleep(2)
            compt= compt + 1
        
        """stop sending image_information"""
        self.set_send_image_formation_state(False)
        
        print("film time end")
        return True
        
    def _create_client(self, ip, port):
        """create an UDP client on port and ip"""
        self.client = client_OSC_seance(self, ip, port)
    
    def _create_server(self, ip, port):
        """create an UDP client on port and ip"""
        self.server = server_OSC_seance(self, ip, port)
    
    def get_send_image_formation_state(self):
        self._send_image_formation_state[0].acquire()
        state = self._send_image_formation_state[1]
        self._send_image_formation_state[0].release()
        return state
    
    def set_send_image_formation_state(self, state):
        self._send_image_formation_state[0].acquire()
        self._send_image_formation_state[1] = state
        self._send_image_formation_state[0].release()
    
    def get_end_received(self):
        self.end_received[0].acquire()
        state = self.end_received[1]
        self.end_received[0].release()
        return state
    
    def set_end_film(self, state):
        self.end_received[0].acquire()
        self.end_received[1] = state
        self.end_received[0].release()
        
    

    
    def run(self):
        """start sending image information, once every 10 sec"""
        self.set_send_image_formation_state(True)
        fake_comp = 0
        print('start sending formation information')
        while self.get_send_image_formation_state() : 
            print('sending formation information')
            #self.client.send_seance_image_formation(self.current_state.get_image_formation())
            self.client.send_seance_image_formation(fake_comp)
            fake_comp = fake_comp +1
            time.sleep(3)
           
        
     
        
if __name__ == "__main__":
    com_ard = com_arduino()
    cu_state = current_state(com_ard)
    seance_cont = seance_controller(cu_state)
    
    seance_cont.film_begin()
    