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
        self.dispatcher.map("image_capture", print)
        self.dispatcher.map("/show_curve", self.show_curve)

        self.server = osc_server.ThreadingOSCUDPServer((self.ip, self.port), self.dispatcher)
        
        """minimal time in seconds between two calcul"""
        self.min_laps = 0
        self.old_time = 0
        
        self.start()
        
        
    def reset(self, msg):
        print ("reset")
        self.formation_rate.reset()
        
    def show_curve(self, msg):    
        self.formation_rate.show_steadily_curve()
        
    def formation_rate_mesure(self, msg):
        print (msg)
        """security to prevent of analysing two image to close from each other"""
        
        if self.formation_rate.get_formation_rate_asked() :
            delta = time.time() - self.old_time  
            if delta >= self.min_laps :
                    print("calcul formation")
                    value = self.formation_rate.formation_rate_mesure_percent(msg)
                    self.formation_rate.client_OSC.send_formation_rate(value)
                    self.formation_rate.client_TCP._send("AQ : " + str(value))
                    self.old_time = time.time()
             
            else : 
                print("no calcul formation ")   
        else : 
            print ("formation_rate not asked") 
                
        
        

    
    def run(self):
        """start teh server in a thread"""
        print("Serving on {}".format(self.server.server_address))
        self.server.serve_forever()