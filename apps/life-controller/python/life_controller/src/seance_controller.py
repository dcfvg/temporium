'''
Created on 10 mai 2014

@author: ensadlab
'''
from pythonosc import osc_message_builder
from pythonosc import udp_client
from communication.OSC.client_OSC_seance import * 
from communication.OSC.server_OSC_seance import *
from com_arduino import *
from current_state import *
from starting_capture import *

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
       
        
       
        
        """information about the end of the film received"""
        self._end_film = [threading.Lock(), False]
        
        """at the beginning : 
        - create client, create server
        """
        self._create_client("localhost", 3333)
        self._create_server("localhost", 3334)
        
        """order to send or not information about rate of image formation"""
        self._send_formation_rate_state = [threading.Lock(), False]
        
        
    def film_begin(self):
        print("film time begin in 5 sec")
        time.sleep(5)
        
        """send seance begin"""
        self.client_seance.send_seance_begin()
        
        """
        print("starting exposure")
        capture = starting_capture()
        capture.start()
        """
        """server_OSC_seance is waiting for first photo to begin analysing image and send it """
        
        compt = 0 
        
        """while film not end or timeout = 40 min """
        self.set_end_film(False)
        
        while not self.get_end_film() or compt > 1200:
            time.sleep(2)
            compt= compt + 1
        
        """stop sending image_information"""
        self.set_send_formation_rate_state(False)
        
        print("film time end")
        return True
        
        
    def _create_client(self, ip, port):
        """create an UDP client on port and ip"""
        self.client_seance = client_OSC_seance(self, ip, port)
    
    def _create_server(self, ip, port):
        """create an UDP client on port and ip"""
        self.server_seance = server_OSC_seance(self, ip, port)
    
    def get_send_formation_rate_state(self):
        """return send_formation_rate_state"""
        self._send_formation_rate_state[0].acquire()
        state = self._send_formation_rate_state[1]
        self._send_formation_rate_state[0].release()
        return state
    
    def set_send_formation_rate_state(self, state):
        """set send_formation_rate_state"""
        self._send_formation_rate_state[0].acquire()
        self._send_formation_rate_state[1] = state
        self._send_formation_rate_state[0].release()
    
    def get_end_film(self):
        """return en_received"""
        self._end_film[0].acquire()
        state = self._end_film[1]
        self._end_film[0].release()
        return state
    
    def set_end_film(self, state):
        """set _end_fil"""
        self._end_film[0].acquire()
        self._end_film[1] = state
        self._end_film[0].release()
        
    

    
    def run(self):
        if True : 
            """if client_formation_rate connected"""
            """ask client_formation_rate to begin to analyse photo"""
            print ("begin formation rate asked")
            
            """start sending image information, once every 10 sec"""
            self.set_send_formation_rate_state(True)
            fake_comp = 0
            print('start sending formation information')
            while self.get_send_formation_rate_state() : 
                print('sending formation information')
                
                """real function to call"""
                #self.client.send_seance_formation_rate(self.current_state.get_formation_rate())
                
                """for testing"""
                self.client_seance.send_seance_formation_rate(fake_comp)
                fake_comp = fake_comp +1
                time.sleep(3)
                
            """stop asking information"""
            print ("end formation rate asked")
        else : 
            print ("client_formation_rate not connected")
        if False : 
            """if client_formation_rate connected"""
            if self.current_state.server.client_connected["server_formation_rate"][1] : 
                """ask client_formation_rate to begin to analyse photo"""
                self.current_state.server.client_connected["server_formation_rate"][0].start_information()
                
                """start sending image information, once every 10 sec"""
                self.set_send_formation_rate_state(True)
                fake_comp = 0
                print('start sending formation information')
                while self.get_send_formation_rate_state() : 
                    print('sending formation information')
                    
                    """real function to call"""
                    #self.client.send_seance_formation_rate(self.current_state.get_formation_rate())
                    
                    """for testing"""
                    self.client_seance.send_seance_formation_rate(fake_comp)
                    fake_comp = fake_comp +1
                    time.sleep(3)
                    
                """stop asking information"""
                self.current_state.server.client_connected["server_formation_rate"][0].stop_information()
            else : 
                print ("client_formation_rate not connected")
           
        
     
        
if __name__ == "__main__":
    com_ard = com_arduino()
    cu_state = current_state(com_ard)
    seance_cont = seance_controller(cu_state)
    
    seance_cont.film_begin()
    