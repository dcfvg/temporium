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

        """stop the cycle, False : not stopped"""
        self._stop = [threading.Lock(), True]
        
        """time between two check"""
        self.time_laps = 1
        
        self.start()
        
        
    def run(self):
        while True :
            while not self.get_stop() :
                name = "BR1"
                if not self.current_state.get_state_EL(name,"MAX") =="NULL" :
                    if self.current_state.get_state_EL(name,"MAX") : 
                        print ("WARNING : " +name+ " boiled over ")
                        self.current_state.kill_all()
                else : 
                    print ("El " + name + " MAX not connected")
                
                name = "BR2"
                if not self.current_state.get_state_EL(name,"MAX") =="NULL" :
                    if self.current_state.get_state_EL(name,"MAX") : 
                        print ("WARNING : " +name+ " boiled over ")
                        self.current_state.kill_all()
                else : 
                    print ("El " + name + " MAX not connected")
                
                name = "BR3"
                if not self.current_state.get_state_EL(name,"MAX") =="NULL" :
                    if self.current_state.get_state_EL(name,"MAX") : 
                        print ("WARNING : " +name+ " boiled over ")
                        self.current_state.kill_all()
                else : 
                    print ("El " + name + " MAX not connected")
                
                name = "BU1"
                if not self.current_state.get_state_EL(name,"MAX") =="NULL" :
                    if self.current_state.get_state_EL(name,"MAX") : 
                        print ("WARNING : " +name+ " boiled over ")
                        self.current_state.kill_all()
                else : 
                    print ("El " + name + " MAX not connected")
                
                name = "BU2"
                if not self.current_state.get_state_EL(name,"MAX") =="NULL" :
                    if self.current_state.get_state_EL(name,"MAX") : 
                        print ("WARNING : " +name+ " boiled over ")
                        self.current_state.kill_all()
                else : 
                    print ("El " + name + " MAX not connected")
                
                name = "BU3"
                if not self.current_state.get_state_EL(name,"MAX") =="NULL" :
                    if self.current_state.get_state_EL(name,"MAX") : 
                        print ("WARNING : " +name+ " boiled over ")
                        self.current_state.kill_all()
                else : 
                    print ("El " + name + " MAX not connected")
                
                name = "AQ"
                if not self.current_state.get_state_EL(name,"MAX") =="NULL" :
                    if self.current_state.get_state_EL(name,"MAX") : 
                        print ("WARNING : " +name+ " boiled over ")
                        self.current_state.kill_all()
                else : 
                    print ("El " + name + " MAX not connected")
                    
                time.sleep(self.time_laps)
            
            time.sleep(self.time_laps)
        
        
        
    """return the value of self.stop"""
    def get_stop(self):

        self._stop[0].acquire()
        state = self._stop[1]
        self._stop[0].release()
        return state
    
    """set state to stop, will interrupt the cycle of checking security EL """
    def set_stop(self, state):
            
        self._stop[0].acquire()
        self._stop[1] = state 
        self._stop[0].release()
        
        if state : 
            print("Checking security EL : stop") 
        else : 
            print("Checking security EL : start")
           
    
        
        
        
        
        
    

        
        
