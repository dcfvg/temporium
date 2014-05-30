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
        """wait 300 sec or order to stop"""
        compt = 0 
        while self.current_state.get_keep_going() and compt <300 : 
            time.sleep(1)
            compt = compt + 1
        print("Fin de la filtration automatique")
        self.current_state.set_current_action("filter_aquarium",False)
        
        
    

        
        