'''
Created on Jun 6, 2014

@author: Cactus
'''
import threading
import time
class spectro(object):
    '''
    classdocs
    '''


    def __init__(self, a_current_state):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        self.current_state = a_current_state
        
    def run(self):
        
        if self.current_state.get_client_connected("server_concentration") :
            """start the spectro and wait for a value"""
            self.current_state.set_information_asked("concentration", True)
            while self.current_state.get_spectro_mesure()=="NULL" : 
                time.sleep(1)
                
                
            current_concentration = self.current_state.get_spectro_mesure()
        
    
        