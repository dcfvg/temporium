'''
Created on May 1, 2014

@author: Cactus
'''
import time
import threading

class server_level(threading.Thread):
    '''
    classdocs
    '''

    def __init__(self, client_socket,name):
        
        threading.Thread.__init__(self)
        
        self.client_socket = client_socket
        self.terminated = False 
        self.name = name
        '''
        Constructor
        
        '''
        self.start()
        
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
       
        