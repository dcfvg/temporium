'''
Created on Apr 28, 2014

@author: Cactus
'''
import socket
import time 
import threading


class client(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        
        self.name = "client_analyse_image"
        
        self.connected = False
        self.terminated = False
     
        
        """Socket TCP """
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        if self.client_socket == -1 : 
            print ("Error in socket_server creation ")
        else : 
            print ("Socket_client built")
            """
    def run(self): 
        print(self.name +" start")

        try:
            
            while not self.terminated : 
                
                data = self._recv()
                if data =="" :
                    self.stop()
                else :        
                    print (self.name + " received : "+ data)
                    """do whatever you want"""
        
        except IOError:
            print("not ready")
            
            
    def ask_connection(self, host, port):
        if self.connected : 
            print (self.name + " already connected")
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
                    self.start()
                else : 
                    print("connection refused")
                    self.stop()
            
            except IOError:
                """Send response message for file not found"""
                print("Pb connection")
                print(IOError)
       
    
    def _send(self, msg):
        self.client_socket.send(msg.encode(encoding='utf_8', errors='strict'))
        
    def _recv(self):
        return self.client_socket.recv(1024).decode()
    
    def _close(self) :
        #self.client_socket.shutdown(2)
        self.client_socket.close()
    
    def stop(self) :
        self.terminated = True
        self._close()
        self.connected = False
        print(self.name + "finish") 


if __name__ == "__main__":
    client = client()
    client.ask_connection('localhost', 8000)
    i = input('Choose a number :')
    client._send(i)

    """
    client._send("test client 1")
    time.sleep(1)
    client._send("test client 2")  
    time.sleep(3)
    client._send("test client 3")
    time.sleep(1)
    client._send("test client 2")  
    time.sleep(3)
    client._send("test client 3") 
    time.sleep(1)
    client._send("test client 2")  
    time.sleep(3)
    client._send("test client 3") 
    time.sleep(1)
    client._send("test client 2")  
    time.sleep(3)
    client._send("test client 3") 
    
    """


    
    
    
    
    

