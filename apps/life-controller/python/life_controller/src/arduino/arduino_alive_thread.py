'''
Created on May 24, 2014

@author: Cactus
'''
import threading
import time

class arduino_alive_thread(threading.Thread):
    '''
    thread that check the security electrode_max and stop every process if an EL turns ON (meaning that there is a problem ) 
    '''

    def __init__(self,a_arduino_mega):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)

        self.arduino_mega = a_arduino_mega
        
        """send an alive signal every 3 sec"""
        self.delay_alive = 3
        
        self.start()
        
    def run(self):
        
        while True : 
            self.arduino_mega.alive()
            
            time.sleep(self.delay_alive)
        

           
    
        
        
        
        
        
    

        
        
