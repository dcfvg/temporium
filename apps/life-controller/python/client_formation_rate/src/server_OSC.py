'''
Created on 10 mai 2014

@author: ensadlab
'''
import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server
import time
import threading

class server_OSC(threading.Thread):
    '''
    classdocs
    '''
    

    def __init__(self, un_formation_rate, ip, port):
        '''
        init the dispatcher : what to do dpending on the pattern 
        '''
        
        threading.Thread.__init__(self)
        
        self.formation_rate = un_formation_rate
        
        self.ip = ip 
        self.port= port
        
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/seance_start", self.reset)
        self.dispatcher.map("/image_capture", self.formation_rate_mesure)

        self.server = osc_server.ThreadingOSCUDPServer((self.ip, self.port), self.dispatcher)
        
        """minimal time in seconds between two calcul"""
        self.min_laps = 20
        
        self.start()
        
        
    def reset(self, msg):
        print ("reset")
        self.formation_rate.reset()
        
    def formation_rate_mesure(self, msg):
        print (msg)
        delta = time.time() - self.old_time 
        self.old_time = time.time()
        if delta >= self.min_laps :
            print("calcul formation")
            value = self.formation_rate.formation_rate_mesure(msg)
            self.formation_rate.client_OSC.send_formation_rate(value)
            
            if self.formation_rate.get_formation_rate_asked() : 
                self.formation_rate.client_TCP._send("FORMATION_RATE : value")
        else : 
            print("no calcul formation ")
        

    
    def run(self):
        """start teh server in a thread"""
        print("Serving on {}".format(self.server.server_address))
        self.server.serve_forever()