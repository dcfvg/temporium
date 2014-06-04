'''
Created on May 1, 2014

@author: Cactus
'''
import time
import threading
from current_state import*

class server_concentration(threading.Thread):
    '''
    classdocs
    '''

    def __init__(self, client_socket, un_server):
        
        threading.Thread.__init__(self)
        
        self.client_socket = client_socket
        self.terminated = False 
        self.name = "server_concentration"
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
                
                #print (self.name + " received : "+ data)
                print (self.name + " received " + data )
                data = data.split("\n")
                
                for msg in data : 
                    try : 
                        """information in shape AQ : %,realvalue"""
                        data_list = msg.split(":")
                        
                        container_name = data_list[0].strip()
                        """value = [%,real_value]"""
                        value = data_list[1].split(",")
                        percent = float(value[0].strip())
                        real_value = float(value[1].strip())
                    
                    
                        self.current_state.set_concentration(container_name, percent)
                    
                    except Exception:
                        """Sprint what is wrong"""
                        pass
                        #print(self.name +" Message does not fit the protocol")

    
            
    def _send(self , msg):
        msg = msg + " \n"
        self.client_socket.sendall(msg.encode(encoding='utf_8', errors='strict'))
        
    def _recv(self):
        return self.client_socket.recv(2048).decode()  
    
    def ask_information (self, state):
        if state : 
            self._send("concentration_start") 
        else : 
            self._send("concentration_stop")
        
        
    def stop(self) :
        self.terminated = True
        self._close() 
        self.server.current_state.set_client_connected_state(self.name, False)
        print( self.name +" finish")
    
    def _close(self):
        self.client_socket.close() 
       
        