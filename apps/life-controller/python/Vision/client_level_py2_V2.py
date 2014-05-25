'''
Created on Apr 28, 2014

@author: Cactus
'''
import socket
import time 
import threading
from image_level_V2 import *


class client_level_py2_V2(threading.Thread):

    def __init__(self, an_adress, a_port):
        threading.Thread.__init__(self)
        
        self.name = "client_level"
        
        """adress and port to ask connection"""
        self.adress = an_adress
        self.port = a_port
        
        self.connected = False
        self.terminated = False
        
        """creation of the image object"""
        self.image_level_V2 = image_level_V2(self)
        """to avoid it to start without the order to"""
        self.image_level_V2.lock.acquire()
        """start image object"""
        self.image_level_V2.start()
        
        self.start()
     
      
        
    def run(self): 
        """start to listen"""
        print(self.name +" start")
        
        """condition to kill the client"""
        while not self.terminated :
            """while client is not connected, ask connection every 5 seconds"""
            while not self.connected:
                self.ask_connection(self.adress, self.port)
                time.sleep(5)
            
            try:
                
                while not self.terminated : 
                    
                    """block until data comes"""
                    data = self._recv()
                    
                    """signal that the server is deconnected, so end the connexion"""
                    if data =="" :
                        self.stop()
                    else :        
                        print self.name + " received : "+ data
                        """do whatever you want"""
                        
                        if (data =="level_start"):
                       
                            """order to start"""
                            print "Ask for image analysis"
                            self.image_level_V2.lock.release()
                            print "let Image start running"


                        """if order : stop, set the order tso stop giving level information"""
                        if (data =="level_stop"):
                            """order to start"""
                            """prevent from starting the new thread"""
                            self.image_level_V2.lock.acquire()
            
            except IOError:
                print("not ready")
                
            
    def ask_connection(self, host, port):
        if self.connected : 
            print self.name + " already connected"
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
                    print "connection granted"
                    state =  True
                else : 
                    print "connection refused"
                    self.stop()
                    state = False
            
            except IOError:
                """Send response message for file not found"""
                print "Pb connection : No response from the server"
                #print(IOError)
                state = False
                return state
        return state
            
       
    
    def _send(self, msg):
        # Connection verification before sending a message
        if self.connected:
            self.client_socket.send(msg.encode(encoding='utf_8', errors='strict'))
            return True
        else:
            print "No connection available"
            return False

    def _recv(self):
        return self.client_socket.recv(1024).decode()
    
    def _close(self) :
        #self.client_socket.shutdown(2)
        self.client_socket.close()
    
    def stop(self) :
        self._close()
        self.connected = False
        print self.name + "finish" 


if __name__ == "__main__":
    
    
    client = client_level_py2_V2(localhost, 8000)

   


    
    
    
    
    

