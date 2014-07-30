'''
Created on 10 mai 2014

@author: ensadlab
'''
import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server
import threading

class server_OSC_UI(threading.Thread):
    '''
    classdocs
    '''
    

    def __init__(self, current_state_order, ip, port):
        '''
        init the dispatcher : what to do dpending on the pattern 
        '''
        
        threading.Thread.__init__(self)
        
        self.current_state_order = current_state_order
        
        self.ip = ip 
        self.port= port
        
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/debug", print)
        self.dispatcher.map("/sss", self.sss)

        self.server = osc_server.ThreadingOSCUDPServer((self.ip, self.port), self.dispatcher)
        
        self.start()
        
        
    
    def sss(self, msg):
        """what to do when finished"""
        
        self.seance_controller.set_end_film(True)
        print(msg)
        

    
    def run(self):
        """start teh server in a thread"""
        print("Serving on {}".format(self.server.server_address))
        self.server.serve_forever()