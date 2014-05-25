'''
Created on 11 mai 2014

@author: ensadlab
'''
import threading
import time

class auto_AQ_filtration(threading.Thread):
    '''
    thread to run to start an automatic filtration of AQ, but do not call it directly, use current_state.set_current_action
    '''

    def __init__(self,a_current_state):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)

        self.current_state = a_current_state
        
        
        
    def run(self):
        """set auto filtration to True"""
        self.current_state._set_current_action_evolved("auto_AQ_filtration",True)
        """start filtration"""
        self.current_state.set_current_action("AQ_filtration",True)
        print("Filtration automatique : 5 min")
        """wait 300 sec or order to stop"""
        compt = 0 
        while compt <300 and self.current_state.get_current_action_evolved("auto_AQ_filtration"): 
            time.sleep(1)
            compt = compt + 1
        print("Fin de la filtration automatique")
        """end filtration"""
        self.current_state.set_current_action("AQ_filtration",False)
        """set auto filtration to False"""
        self.current_state._set_current_action_evolved("auto_AQ_filtration",False)
        
        
    

        
        