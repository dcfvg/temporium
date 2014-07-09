'''
Created on Jun 5, 2014

@author: Cactus
'''
import time
import threading

class time_controller(threading.Thread):
    

    def __init__(self, un_current_state):
        '''
    
        
        manage the schedule of the temporium"""
        '''
        
        threading.Thread.__init__ (self, target=self.run)
        self.current_state = un_current_state
        """like [hour, minute]"""
        self.time_start_day = self.current_state.config_manager.get_time_controller("START_DAY")
        self.time_end_day = self.current_state.config_manager.get_time_controller("END_DAY")
        
        print("start time_controller")
        
        
    def run(self):
        compt = 0
        while True :
            print ("time_controller" + str(compt)) 
            compt = compt +1
            if self.current_state.get_current_time_controller_state("renew_heavy_AQ") :
                
                if  self.renew_heavy_AQ_state() and self.expo_open() :
                        
                        print("start cycle heavy for this day")
                        self.current_state.set_current_action_aquarium_evolved("aquarium_cycle_heavy", True)
                        #time.sleep(5)
                        while self.current_state.get_current_action_aquarium_evolved("aquarium_cycle_heavy") : 
                            time.sleep(5) 
                        print("renew cycle heavy done for this day")
                        """set this action to done"""
                        self.current_state.set_daily_action_day("renew_heavy_AQ",int(time.strftime("%d",time. localtime())) )
                        self.current_state.set_daily_action_state("renew_heavy_AQ",True )
                        
                
            
                        
            #print ("renew" + str(self.current_state.get_current_time_controller_state("exposition")))

            if self.current_state.get_current_time_controller_state("exposition") : 
                 
                if self.expo_open() :
                    """start the day with  renew heavy""" 
                    
                    print("Start film")
                    self.current_state.set_current_film_state("film", True)
                    
                    while self.current_state.get_current_film_state("film") : 
                        time.sleep(5)
                    
                    print("End film")
                    
                    print("start cycle light for this day")
                    self.current_state.set_current_action_aquarium_evolved("aquarium_cycle_light", True)
                    #time.sleep(5)
                    while self.current_state.get_current_action_aquarium_evolved("aquarium_cycle_light") : 
                        time.sleep(5) 
                    print("renew cycle light for this day")
            
            
                    
                
                
                
            time.sleep(5)
                
    
    def renew_heavy_AQ_state(self):
        
        #print(self.current_state.get_daily_action_state("renew_heavy_AQ"))
        
        if not (self.current_state.get_daily_action_day("renew_heavy_AQ") == int(time.strftime("%d",time. localtime()))) :
            state = True
        else : 
            state = not self.current_state.get_daily_action_state("renew_heavy_AQ")   
        return state
        
        
    def expo_open(self):
        """get the time and check if the expo is open"""
        """conversion in minute to simplify"""
        time_start_day_minute  = self.time_start_day[0]*60 + self.time_start_day[1]
        time_end_day_minute  = self.time_end_day[0]*60 + self.time_end_day[1]
        
        state = False 
        current_time_minute  = int(time.strftime("%H",time. localtime())) * 60 + int(time.strftime("%M",time. localtime()))
        if  current_time_minute > time_start_day_minute and \
            current_time_minute < time_end_day_minute :
            
            state = True
            
        return state 
            
        