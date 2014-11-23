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
        
        """time_out for the film"""
        self._time_out = None
        
        self._start_lock = threading.Lock()
        self._start_lock.acquire()
        """emergency stop"""

        self.start()
        
    def start_film(self):
        self._stop_film = False
        self._start_lock.release()

    def run(self):
        while True : 
            self._start_lock.acquire()
            self.film_begin()
            self.current_state._set_current_film_state("film",False)
            self.current_state._set_current_film_state("last_sequence",False)
        
    def film_begin(self):
        self._time_out = self.current_state.config_manager.get_film("TIME_OUT")
        print("film time begin")
        self.current_state.saving_state_thread.write_action("Begin seance")
        #time.sleep(5)
        
        print("screen outside down begin")
        self.current_state.set_current_action_lift_screen("screen_down_outside")
        while self.current_state.get_current_action_lift_screen("screen_down_outside") : 
            time.sleep(2)
        print("screen outside down finish")
        
        """send seance begin"""
        self.client_seance.send_seance_begin()
        self.current_state.saving_state_thread.write_action("Begin film") 
        
        """start ask information formation """
        self.current_state.set_information_asked("formation_rate", True)

        """server_OSC_seance is waiting for first photo to begin analysing image and send it """
        
       
        
        start_time = time.time()

        while  (time.time()-start_time) < (self._time_out*60) and self.current_state.get_current_film_state("last_sequence"):
            time.sleep(2)

        """ --------------------------------------------------------------------------------------------"""
        """ --------------------------------------------------------------------------------------------"""
        """ /!\ C'est içi qu'il faut ajouter du temps en secondes, Pour L'instant c'est 20 secondes /!\ """
        """ change time.sleep(2) -> time.sleep(XX) avec l temps en secondes que tu veux ----------------"""
        time.sleep(20)
        

        """ /!\ ------------------------------------------------------------------------------------/!\ """

        """ --------------------------------------------------------------------------------------------"""
        """ --------------------------------------------------------------------------------------------"""
        """ --------------------------------------------------------------------------------------------"""
        """ --------------------------------------------------------------------------------------------"""

        print("screen outside up begin")
        self.current_state.set_current_action_lift_screen("screen_up_outside")
        while self.current_state.get_current_action_lift_screen("screen_up_outside") : 
            time.sleep(2)
        print("screen outside up finish")


        while  (time.time()-start_time) < (self._time_out*60) and self.current_state.get_current_film_state("film"):
            time.sleep(2)            
        
        
        """stop ask information formation """
        self.current_state.set_information_asked("formation_rate", False)
        
        
        self.client_seance.sent_seance_stop()
        print("film time end") 
        self.current_state.saving_state_thread.write_action("End film")         
        
        self.current_state.saving_state_thread.write_action("End seance")
    def _create_client(self, ip, port):
        """create an UDP client on port and ip"""
        self.client_seance = client_OSC_seance(self, ip, port)
    
    def _create_server(self, ip, port):
        """create an UDP client on port and ip"""
        self.server_seance = server_OSC_seance(self, ip, port)

    
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
        

    