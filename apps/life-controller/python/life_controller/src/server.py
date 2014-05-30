'''
Created on Apr 28, 2014

@author: Cactus
'''
import socket
import threading
import time
from server_level import *
from server_arduino_order import *

class server(threading.Thread) : 
    
    
    def __init__(self, host, port, cu_state):
        
        threading.Thread.__init__(self)
        
        """set this boolean to True to kill the thread"""
        self.terminated = False
        
        self.host = host 
        self.port = port
        self.name = "server_connection"
        self.number = 0 
        
        self.current_state = cu_state
        
        """Socket TCP """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        if self.server_socket == -1 : 
            print ("Error in server_socket creation ")
        else : 
            print ("server_socket built")
            
        """dictionnary of all client connected to the server"""
        
        self.client_connected = dict()
        
        
   
    
    def run(self): 
        
        print(self.name +" start")

        """Set port, and adress"""
        self.server_socket.bind((self.host, self.port))
        
        """listen for attempt to connect"""
        self.server_socket.listen(5)
        
        """Enable to kill the thread in a good way"""
        while not self.terminated :
            
            """wait until a client asks a connection and accept it"""
            print("Server waiting for connection")
            client_socket, address_client = self.server_socket.accept()
            print("Connexion asked by " + address_client[0])
            
            
            """stay in the loop in case of a problem with trash data received"""
            
            while True : 
                first_contact_data = self._recv(client_socket)
                #print("server boucle")
                if first_contact_data != "" : 
                    break
            print("Asking for connection from : " + first_contact_data)
            
            #print(first_contact_data)
            
            if first_contact_data =="client_analyse_image":
                self._send(client_socket,"OK")
                self.number +=1
                the_server_level = server_level(client_socket,str(self.number))
                self.client_connected["client_analyse_image"] = the_server_level
            
    
            elif first_contact_data =="client_level":
                self._send(client_socket,"OK")
                self.number +=1
                the_server_level = server_level(client_socket,"client_analyse_image "+ str(self.number),self.current_state)
                self.client_connected["client_analyse_image"] = the_server_level
            
            elif first_contact_data =="client_arduino_order":
                self._send(client_socket,"OK")
                self.number +=1
                the_server_arduino_order = server_arduino_order(client_socket,"client_arduino_order" + str(self.number),self.current_state)
                self.client_connected["client_arduino_order"] = the_server_arduino_order    
            
            else : 
                self._send(client_socket,"NO")
                
            
            
            
            
    def _send(self, socket , msg):
        socket.sendall(msg.encode(encoding='utf_8', errors='strict'))
        
    def _recv(self, socket):
        return socket.recv(1024).decode()   

    """def client connected to the serveur programme"""    
    def client_connected(self, name, state): 
        self.client_connected[name] = state
        
    def stop(self) :
        self.terminated = True
        self._close()
        print(self.name + "finish") 
    
    def _close(self):
        self.server_socket.close()  
        
        
      
if __name__ == "__main__":
    server = server('', 8001)
    server.start()
    
    
    

    
    
"""

You are experiencing the TIME_WAIT state of connected sockets. Even though you've closed your socket, it still has lingering consequences for a couple minutes. The reasons for this, as well as a socket flag you can set to disable the behavior (SO_REUSEADDR), are explained in the UNIX guide socket FAQ.

In short,

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

"""
    
    

    
