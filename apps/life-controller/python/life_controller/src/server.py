'''
Created on Apr 28, 2014

@author: Cactus
'''
import socket
import threading
import time
from server_level import *
from server_arduino_order import *
from server_concentration import *
from server_formation_rate import *

class server(threading.Thread) : 
    
    
    def __init__(self, host, port, cu_state):
        
        threading.Thread.__init__(self)
        
        """set this boolean to True to kill the thread"""
        self.terminated = False
        
        self.host = host 
        self.port = port
        self.name = "server_connection"
        
        """keep the compt of connection asked"""
        self.number = 0 
        
        self.current_state = cu_state
        
        """Socket TCP """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        if self.server_socket == -1 : 
            print ("Error in server_socket creation ")
        else : 
            print ("server_socket built")
            
        """dictionnary of all client connected to the server"""
        
        """list of server in charge of the communication"""
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
            
            if first_contact_data =="client_formation_rate":
                """if it is the first time"""
                if not "server_formation_rate" in self.client_connected :
                    self._send(client_socket,"OK")
                    the_server_formation_rate = server_formation_rate(client_socket, self)
                    self.client_connected["server_formation_rate"] = [the_server_formation_rate, True]
                    self.number +=1
                    print("server_formation_rate accepted")
                    """ if the server is down, new connection"""
                elif not self.client_connected["server_formation_rate"][1] : 
                    self._send(client_socket,"OK")
                    the_server_formation_rate = server_formation_rate(client_socket, self)
                    self.client_connected["server_formation_rate"] = [the_server_formation_rate, True]
                    self.number +=1
                    print("server_formation_rate accepted")
                    """ if the server is ok, no new connection possible"""
                else : 
                    self._send(client_socket,"NO")
                    print("server_formation_rate refused")
                    
            
    
            elif first_contact_data =="client_level":
                """if it is the first time"""
                if not "server_level" in self.client_connected :
                    self._send(client_socket,"OK")
                    the_server_level = server_level(client_socket, self)
                    self.client_connected["server_level"] = [the_server_level, True]
                    self.number +=1
                    print("server_level accepted")
                  
                    """ if the server is down, new connection"""
                elif not self.client_connected["server_level"][1] : 
                    self._send(client_socket,"OK")
                    the_server_level = server_level(client_socket, self)
                    self.client_connected["server_level"] = [the_server_level, True]
                    self.number +=1
                    print("server_level accepted")
                    
                    """ if the server is ok, no new connection possible"""
                else : 
                    self._send(client_socket,"NO")
                    print("server_level refused")
    
            
            elif first_contact_data =="client_concentration":
                """if it is the first time"""
                if not "server_concentration" in self.client_connected :
                    self._send(client_socket,"OK")
                    the_server_concentration = server_concentration(client_socket, self)
                    self.client_connected["server_concentration"] = [the_server_concentration, True]
                    self.number +=1
                    print("server_concentration accepted")
                  
                    """ if the server is down, new connection"""
                elif not self.client_connected["server_concentration"][1] : 
                    self._send(client_socket,"OK")
                    the_server_concentration = server_concentration(client_socket, self)
                    self.client_connected["server_concentration"] = [the_server_concentration, True]
                    self.number +=1
                    print("server_concentration accepted")
                    
                    """ if the server is ok, no new connection possible"""
                else : 
                    self._send(client_socket,"NO")
                    print("server_concentration refused")
                
                
                """for test purposes"""
            elif first_contact_data =="client_arduino_order":
                """if it is the first time"""
                if not "server_arduino_order" in self.client_connected :
                    self._send(client_socket,"OK")
                    the_server_arduino_order = server_arduino_order(client_socket, self)
                    self.client_connected["server_arduino_order"] = [the_server_arduino_order, True]
                    self.number +=1
                    print("server_arduino_order accepted")
                  
                    """ if the server is down, new connection"""
                elif not self.client_connected["server_arduino_order"][1] : 
                    self._send(client_socket,"OK")
                    the_server_arduino_order = server_arduino_order(client_socket, self)
                    self.client_connected["server_arduino_order"] = [the_server_arduino_order, True]
                    self.number +=1
                    print("server_arduino_order accepted")
                    
                    """ if the server is ok, no new connection possible"""
                else : 
                    self._send(client_socket,"NO")
                    print("server_arduino_order refused")
            
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
    
    

    
