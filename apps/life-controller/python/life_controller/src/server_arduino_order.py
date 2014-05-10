'''
Created on May 1, 2014

@author: Cactus
'''
import time
import threading

class server_arduino_order(threading.Thread):
    '''
    classdocs
    '''

    def __init__(self, client_socket,name, un_current_state):
        
        threading.Thread.__init__(self)
        
        self.client_socket = client_socket
        self.terminated = False 
        self.name = name
        '''
        Constructor
        
        '''
        self.start()
        
        """com_arduino"""
        self.com_arduino = un_current_state.com_arduino
        
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
        print( self.name +" finish")
    
    def _close(self):
        self.client_socket.close() 
       
        