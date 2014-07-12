'''
Created on Jul 8, 2014

@author: Cactus
'''

import threading 
import os
import signal
import time


class saving_state_thread (threading.Thread):

    def __init__ (self, un_current_state):
      
        threading.Thread.__init__ (self, target=self.run)
        
        self.current_state = un_current_state
        
        self._saving_action_url = self.current_state.config_manager.get_saving("action_time")
        self.file_action = open(self._saving_action_url +"/action_done"+ time.strftime("%d_%b_%Y_%H:%M:%S",time. localtime())+".txt","w")


    def run(self):
        while True : 
            self.write_curren_situation()
            time.sleep (2)
            
    def write_curren_situation(self):
        
        save_file = open ("save_current_situation/last_state.txt", "w")
        save_file.write("Temporium : last_situation "+ " \n")
        
        for item in self.current_state._occupied_volume : 
            save_file.write("occupied_volume : "+ item + " : " + str(self.current_state.get_occupied_volume(item)) + " \n")
    
        for item in self.current_state._daily_action : 
            save_file.write("daily_action : "+ item + " : " + str(self.current_state.get_daily_action_state(item)) + " : " + str(self.current_state.get_daily_action_day(item)) + " \n")

        save_file.flush()
        
    def write_action(self, action_string):
        self.file_action.write(time.strftime("%d_%b_%Y_%H:%M:%S",time. localtime()) + " : "+ action_string +"\n")
        self.file_action.flush()
    
    
        