'''
Created on May 1, 2014

@author: Cactus
'''
import time
import threading
from current_state import*

class server_level(threading.Thread):
    '''
    classdocs
    '''

    def __init__(self, client_socket,name, current_state):
        
        threading.Thread.__init__(self)
        
        self.client_socket = client_socket
        self.terminated = False 
        self.name = name
        '''
        Constructor
        
        '''
        """current_state"""
        self.current_state = current_state
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
                """information like '{'M1': 3, 'M2': 2} ' """
                #print (self.name + " received : "+ data)
                data_list = data.split("\n")
                msg = data_list[0]
                msg = msg.replace("{", "")
                msg = msg.replace("}","")
                volume_cont_list = msg.split(",")
                try:
                
                    for item in volume_cont_list : 
                        """info like ' 'M1': 3 '"""
                        info = item.strip().split(":")
                        
                        cont =info[0].strip().replace("'","") 
                        vol = info[1].strip()
                        self.current_state.set_occupied_volume(cont.strip(), float(vol))
                        #print("V " + cont +" = " + vol + " set")
                    #print (self.name + " received OK : "+ data)
                    #print("msg OK ")
                except Exception:
                    """Sprint what is wrong"""
                    print(self.name +" Message does not fit the protocol")
                    #print( self.name + " received WRONG : "+ msg)
                    pass

    
            
    def _send(self , msg):
        self.client_socket.sendall(msg.encode(encoding='utf_8', errors='strict'))
        
    def _recv(self):
        return self.client_socket.recv(2048).decode()   
        
        
    def stop(self) :
        self.terminated = True
        self._close() 
        print( self.name +" finish")
    
    def _close(self):
        self.client_socket.close() 
       
        