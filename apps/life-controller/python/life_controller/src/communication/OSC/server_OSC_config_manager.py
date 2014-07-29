'''
Created on 10 mai 2014

@author: ensadlab
'''
import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server
import threading
class server_OSC_config_manager(threading.Thread):
    '''
    classdocs
    '''
    

    def __init__(self, a_config_manager, ip, port):
        '''
        init the dispatcher : what to do dpending on the pattern 
        '''
        
        threading.Thread.__init__(self)
       
        self.name = "server_OSC_config_manager"
        self.config_manager = a_config_manager
        
        self.ip = ip 
        self.port= port
        
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/debug", print)
        self.dispatcher.map("/refresh_config", self.refresh_config)

        self.server = osc_server.ThreadingOSCUDPServer((self.ip, self.port), self.dispatcher)
        
        self.start()
        
        
    """refresh config in config_manager"""
    def refresh_config(self):
        self.config_manager.read_config()
    
    def run(self):
        """start teh server in a thread"""
        print(self.name + " Serving on {}".format(self.server.server_address))
        self.server.serve_forever()
    
