'''
Created on May 1, 2014

@author: Cactus

Need to be adapted because, is made to deal with level_fake    
'''
import time
import threading
from current_state import*

class server_level(threading.Thread):
    '''
    classdocs
    '''

    def __init__(self, client_socket, un_server):
        
        threading.Thread.__init__(self)
        
        self.client_socket = client_socket
        self.terminated = False 
        self.name = "server_level"
        '''
        Constructor
        
        '''
        self.server = un_server
        """current_state"""
        self.current_state = self.server.current_state

        self.start()
        
        "ask for information"
        self._send("level_start")
      
        
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
                """information like 'M1: 3, M2: 2 \n ' """
                #print (self.name + " received : "+ data)
                data = data.split("\n")
                
                for msg in data : 
                    
                    volume_cont_list = msg.split(",")
                    #print ("message " +str(volume_cont_list) )
                    #print ("daz " +str(volume_cont_list) )
                    
                    """try"""
                    for item in volume_cont_list : 
                        """info like ' M1 : 3 '"""
                        #print ("message " +str(item) )
                        info = item.split(":")
                        #print ("info " +str(info) )
                        try :
                            cont =info[0].strip()
                            vol = info[1].strip()
                            #print (cont + " " + vol )
                            
                            if not vol == "null" :
                                self.current_state.set_occupied_volume(cont, float(vol))
                                #print("volume "+ cont.strip() + " set to " +vol)
                            
                                
                            else : 
                                print ("message daz" + cont + " "  + vol)
                        except Exception:

                            #print(self.name +" Message does not fit the protocol " + msg)
                            pass
                    """except Exception:

                        print(self.name +" Message does not fit the protocol " + msg)"""
                        
                        
    def begin_information(self):
        self._send("level_start \n")
    
    def end_information(self):
        self._send("level_stop \n")
    
            
    def _send(self , msg):
        self.client_socket.sendall(msg.encode(encoding='utf_8', errors='strict'))
        
    def _recv(self):
        return self.client_socket.recv(2048).decode()   
    
    
        
    def stop(self) :
        self.terminated = True
        self._close() 
        self.server.client_connected[self.name][1]= False
        print( self.name +" finish")
    
    def _close(self):
        self.client_socket.close() 
       
        