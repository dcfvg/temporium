'''
Created on May 1, 2014

@author: Cactus
'''
import time
import threading

class server_arduino_order(threading.Thread):
    '''
    server to send information that arduino received to simulate the arduino
    '''

    def __init__(self, client_socket, un_server):
        
        threading.Thread.__init__(self)
        
        self.client_socket = client_socket
        self.terminated = False 
        self.name = "server_arduino_order"
        '''
        Constructor
        
        '''
        self.server = un_server
        """current_state"""
        self.current_state = self.server.current_state
        """com_arduino"""
        self.com_arduino = self.current_state.com_arduino
        
        self.start()
        
        
        
        """set this server in com_arduino"""
        self.com_arduino.set_server_arduino_order(self)
        
        
    def run(self): 
        """start to listen"""
        print(self.name +" start")
        
        while not self.terminated : 
            
            
            """block until data comes"""
            data = self._recv()
            
            """signal that the server is deconnected, so end the connexion"""
            if data =="" :
                self.stop()
            else :        
                print (self.name + " received : "+ data)
         
    
            
    def _send(self , msg):
        self.client_socket.sendall(msg.encode(encoding='utf_8', errors='strict'))
        
    def _recv(self):
        return self.client_socket.recv(1024).decode()   
        
        
    def stop(self) :
        self.terminated = True
        self._close() 
        self.server.client_connected[self.name][1]= False
        print( self.name +" finish")
    
    def _close(self):
        self.client_socket.close() 
       
        