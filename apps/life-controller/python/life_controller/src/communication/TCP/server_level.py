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
        
        """lock to be sure to not send several message at the same time"""
        self.lock_message = threading.Lock()

        self.start()
        
      
        
    def run(self): 
        print(self.name +" start")
        
        while not self.terminated : 
            
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
                                #print ("message null" + cont + " "  + vol)
                                pass
                                
                        except Exception:

                            #print(self.name +" Message does not fit the protocol " + msg)
                            pass
                    """except Exception:

                        print(self.name +" Message does not fit the protocol " + msg)"""
                        
                        
    def ask_information (self, state):
        if state : 
            self._send("level_start") 
        else : 
            self._send("level_stop")
    
            
    def _send(self , msg):
        if not self.terminated : 
            try : 
                msg = msg + " \n"
                self.lock_message.acquire()
                self.client_socket.sendall(msg.encode(encoding='utf_8', errors='strict'))
                self.lock_message.release()
            except Exception as e : 
                print(str(e))
        
    def _recv(self):
        return self.client_socket.recv(2048).decode()   
    
    
        
    def stop(self) :
        self.terminated = True
        self._close() 
        self.server.current_state.set_client_connected_state(self.name, False)
        print( self.name +" finish")
    
    def _close(self):
        self.client_socket.close() 
       
        