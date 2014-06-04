'''
Created on May 1, 2014

@author: Cactus
'''
import time
import threading
from current_state import*

class server_formation_rate(threading.Thread):
    '''
    classdocs
    '''

    def __init__(self, client_socket, un_server):
        
        threading.Thread.__init__(self)
        
        self.client_socket = client_socket
        self.terminated = False 
        self.name = "server_formation_rate"
        '''
        Constructor
        
        '''
        """current_state"""
        self.server = un_server
        """current_state"""
        self.current_state = self.server.current_state

        self.start()
        
        "ask for information"
        #self._send("concentration_start")
      
        
    def run(self): 
        print(self.name +" start")
        
        while not self.terminated : 
            """
            while True : 
                data = self._recv()
                print("boucle")
                if data !="" : 
                    break
            """
            
            
            data = self._recv()
            if data =="" :
                self.stop()
            else :        
                """information like 'AQ : 100 \n ' """
                #print (self.name + " received : "+ data)
                print (self.name + " received " + data )
                data = data.split("\n")
                
                for msg in data : 
                    data_list = msg.split(":")
                    container_name = data_list[0].strip()
                    value = data_list[1].strip()
                    try:
                        self.current_state.set_formation_rate( float(value))
                    
                    except Exception:
                        """Sprint what is wrong"""
                        print(self.name +" Message does not fit the protocol")
                        

    
            
    def _send(self , msg):
        msg = msg + "\n"
        self.client_socket.sendall(msg.encode(encoding='utf_8', errors='strict'))
        
    def _recv(self):
        return self.client_socket.recv(2048).decode()   
     
    def ask_information (self, state):
        if state : 
            self._send("formation_rate_start") 
        else : 
            self._send("formation_rate_stop")
           
        
    def stop(self) :
        self.terminated = True
        self._close() 
        self.server.current_state.set_client_connected_state(self.name, False)
        print( self.name +" finish")
    
    def _close(self):
        self.client_socket.close() 
       
        