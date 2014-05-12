'''
Created on 11 mai 2014

@author: ensadlab
'''
import threading
import time

class auto_filtration(threading.Thread):
    '''
    thread to run action
    '''

    def __init__(self,a_current_state):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)

        self.current_state = a_current_state
        
        
        
    def run(self):
        self.current_state.set_current_action("filter_aquarium",True)
        print("Filtration automatique : 5 min")
        time.sleep(3)
        print("Fin de la filtration automatique")
        self.current_state.set_current_action("filter_aquarium",False)
        
        
    

        
        