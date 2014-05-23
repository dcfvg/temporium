'''
Created on 10 mai 2014

@author: ensadlab
'''
import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server
import threading
class server_OSC_seance(threading.Thread):
    '''
    classdocs
    '''
    

    def __init__(self, un_seance_controller, ip, port):
        '''
        init the dispatcher : what to do dpending on the pattern 
        '''
        
        threading.Thread.__init__(self)
        
        self.seance_controller = un_seance_controller
        
        self.ip = ip 
        self.port= port
        
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/debug", print)
        self.dispatcher.map("/seance_end", self._seance_end)
        self.dispatcher.map("/action", self._action)

        self.server = osc_server.ThreadingOSCUDPServer((self.ip, self.port), self.dispatcher)
        
        self.start()
        
        
    
    def _seance_end(self, msg):
        """what to do when finished"""
        
        self.seance_controller.set_end_film(True)
        print(msg)
        
    
    def _action(self, order):
        """what to do when action asked"""
        print(order)
    
    def run(self):
        """start teh server in a thread"""
        print("Serving on {}".format(self.server.server_address))
        self.server.serve_forever()