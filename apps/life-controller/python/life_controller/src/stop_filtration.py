'''
Created on 11 mai 2014

@author: ensadlab
'''
import threading
import time

class stop_filtration(threading.Thread):
    '''
    thread to run action
    '''


    def __init__(self,a_current_state, a_name):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)

        self.name = a_name
        self.current_state = a_current_state
        
        
    def run(self):
        print("Arret des pompes de retour dans l'aquarium dans : 3 min")
        time.sleep(60)
        print("Arret des pompes de retour dans l'aquarium dans : 2 min")
        time.sleep(60)
        print("Arret des pompes de retour dans l'aquarium dans : 1 min")
        time.sleep(60)
        print("Arret des pompes de retour dans l'aquarium.")
        self.current_state.P_FI_AQ_1(False)
        self.current_state.P_FI_AQ_3(False)
        self.current_state._set_current_action(self.name, False)
        
    

        
        