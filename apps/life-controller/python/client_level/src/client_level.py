'''
Created on Apr 28, 2014
 
@author: Cactus
'''
import socket
import time
import threading
from image_level import *


 
class client_level(threading.Thread):
 
    def __init__(self, adress, port):
        threading.Thread.__init__(self)
         
        self.name = "client_level"
         
        self.connected = False
        self.terminated = False
        
        self.adress = adress
        self.port = port

        """Creation of the object image_spectro"""
         

        self.image_level = image_level(self)

        

        
        
        self.start()

    
    def run(self): 
        """start to listen"""
        print(self.name +" start")
        
        """condition to kill the client"""
        while not self.terminated :
            """while client is not connected, ask connection every 5 seconds"""
            while not self.connected and not self.terminated :
                self.ask_connection(self.adress, self.port)
                time.sleep(5)
            
            
            try:
                
                while self.connected : 
                    
                    """block until data comes"""
                    data = self._recv()
                    
                    """signal that the server is deconnected, so end the connexion"""
                    if data =="" :
                        self.stop_until()
                    else :   
                             
                        data = data.split("\n")
                    
                        for item in data :
                            #print(self.name + " received" + item)
                            try : 
                                if item.strip() == "level_start" :
                                    print("Ask for starting image analysis")
                                    self.image_level.start_level()
                                
                                elif item.strip() == "level_stop" :
                                    print("Ask for stoping image analysis")
                                    self.image_level.stop_level()
                                
                                else : 
    
                                    """Print something is wrong"""
                                    #print(self.name + " Message unknown " + item)
                                    pass
                            except Exception:
                                """Sprint what is wrong"""
                                print(self.name + " Message does not fit the protocol")
            
            except IOError:
                print("not ready")
                
            
    def ask_connection(self, host, port):
        if self.connected : 
            print (self.name + " already connected")
            state = False
        else : 
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
                self.client_socket.connect((host, port))
                self.connected = True
                
                """asking for connection"""
                self._send(self.name)
                
                """wating for an answer"""
                data = self._recv()
                
                if data =="OK" : 
                    print("connection granted")
                    state =  True
                else : 
                    print("connection refused")
                    self.stop()
                    state = False
            
            except IOError:
                """Send response message for file not found"""
                print("Pb connection : No response from the server")
                #print(IOError)
                state = False
                return state
        return state
            
       
    
       
    def _send(self, msg):
        """verify that the connection is available"""
        if self.connected : 
            msg = msg + "\n"
            self.client_socket.send(msg.encode(encoding='utf_8', errors='strict'))
            return True
        else : 
            print("no connection available")
            return False 
        
    def _recv(self):
        return self.client_socket.recv(1024).decode()
     
    def _close(self) :
        #self.client_socket.shutdown(2)
        self.client_socket.close()
 
    def stop_until(self) :
        self.image_level.stop_level()
        self.connected = False
        print (self.name + "finish") 
           
    def stop(self) :
        self.terminated = True
        self._close()
        self.connected = False
        self.image_level.stop_level()
        print (self.name + "finish")
 
 

