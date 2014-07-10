'''
Created on May 24, 2014

@author: Cactus
'''
import threading
import time

class security_EL(threading.Thread):
    '''
    thread that check the security electrode_max and stop every process if an EL turns ON (meaning that there is a problem ) 
    '''

    def __init__(self,a_current_state):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)

        self.current_state = a_current_state
        
        """time between two check"""
        self.time_laps = 1
        
        """set to True if there is a pb"""
        self.boiling_over = False
        """lock to start/stop the thread"""
        self.lock_start = threading.Lock()
        self.lock_start.acquire()
        
        self.start()
        
        
    def run(self):
        while True :
            
            self.lock_start.acquire()
            """no probleme at the beginning"""
            self.boiling_over = False
            
            name = "BR1"
            if not self.current_state.get_state_EL(name,"MAX") =="NULL" :
                if self.current_state.get_state_EL(name,"MAX") : 
                    print ("WARNING : " +name+ " boiled over ")
                    """there is a pb"""
                    self.boiling_over = True
            
            name = "BR2"
            if not self.current_state.get_state_EL(name,"MAX") =="NULL" :
                if self.current_state.get_state_EL(name,"MAX") : 
                    print ("WARNING : " +name+ " boiled over ")
                    """there is a pb"""
                    self.boiling_over = True
            
            name = "BR3"
            if not self.current_state.get_state_EL(name,"MAX") =="NULL" :
                if self.current_state.get_state_EL(name,"MAX") : 
                    print ("WARNING : " +name+ " boiled over ")
                    """there is a pb"""
                    self.boiling_over = True
            
            name = "BU1"
            if not self.current_state.get_state_EL(name,"MAX") =="NULL" :
                if self.current_state.get_state_EL(name,"MAX") : 
                    print ("WARNING : " +name+ " boiled over ")
                    """there is a pb"""
                    self.boiling_over = True
            
            name = "BU2"
            if not self.current_state.get_state_EL(name,"MAX") =="NULL" :
                if self.current_state.get_state_EL(name,"MAX") : 
                    print ("WARNING : " +name+ " boiled over ")
                    """there is a pb"""
                    self.boiling_over = True
            
            name = "BU3"
            if not self.current_state.get_state_EL(name,"MAX") =="NULL" :
                if self.current_state.get_state_EL(name,"MAX") : 
                    print ("WARNING : " +name+ " boiled over ")
                    """there is a pb"""
                    self.boiling_over = True
            
            name = "AQ"
            if not self.current_state.get_state_EL(name,"MAX") =="NULL" :
                if self.current_state.get_state_EL(name,"MAX") : 
                    print ("WARNING : " +name+ " boiled over ")
                    """there is a pb"""
                    self.boiling_over = True
            
            self.lock_start.release()
            
            """if there has been a pb : """
            if self.boiling_over : 
                self.action_emergency()
                
            time.sleep(self.time_laps)
        

    """action to do in case of emergency probleme"""
    def action_emergency(self):
        """disable checking securtity EL to resolve the probleme"""  
        self.current_state.set_security_checking("EL_max", False)
        self.current_state.kill_all()
        
           
    
        
        
        
        
        
    

        
        
