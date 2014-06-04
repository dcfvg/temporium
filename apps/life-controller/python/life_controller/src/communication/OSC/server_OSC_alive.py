'''
Created on 10 mai 2014

@author: ensadlab
'''
import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server
from communication.OSC.client_OSC_alive import *
import threading
class server_OSC_alive(threading.Thread):
    '''
    classdocs
    '''
    

    def __init__(self, un_seance_controller, ip, port):
        '''
        init the dispatcher : what to do dpending on the pattern 
        '''
        
        threading.Thread.__init__(self)
        
        self.ip = ip 
        self.port= port
        
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/debug", print)
        self.dispatcher.map("/alive", self.answer_alive)

        self.server = osc_server.ThreadingOSCUDPServer((self.ip, self.port), self.dispatcher)
        self.client = client_OSC_alive()
        
        self.start()
        
        
    """send an alive message"""
    def _answer_alive(self):
        
        self.client.send_alive()

        
