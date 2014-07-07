'''
Created on Jul 7, 2014

@author: Cactus
'''
import threading 
import os
import time

class thread_image_level(threading.Thread):


    def __init__(self,un_image_level):
        
        self.image_level = un_image_level
        threading.Thread.__init__(self)
        
        
    
    def run(self):
        

        #ne rentrer dans le while que si les coordonnees ne sont pas toutes nulles et si la calibration a ete faite?

        while self.image_level.get_running_state():
            
            self.image_level.analyse_run()
            
            