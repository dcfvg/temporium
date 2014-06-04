'''
Created on May 1, 2014

@author: Cactus
'''
import time
import threading

class server_arduino_order(threading.Thread):
    '''
    server to send information that arduino received to simulate the arduino
    '''

    def __init__(self, client_socket, un_server):
        
        threading.Thread.__init__(self)
        
        self.client_socket = client_socket
        self.terminated = False 
        self.name = "server_arduino_order"
        '''
        Constructor
        
        '''
        self.server = un_server
        """current_state"""
        self.current_state = self.server.current_state
        """com_arduino"""
        self.com_arduino = self.current_state.com_arduino
        
        """lock to be sure to not send several message at the same time"""
        self.lock_message = threading.Lock()
        self.start()
        
        """state of EL receivde : 
        first lock : to unlock when infomation is ready to be read bu aswer_EL
        second lock, when inforamtion has been read and can be rewritten"""
        self._state_EL_received = [threading.Lock(),threading.Lock(), "name_container", "name_EL", "status" ]
        self._state_EL_received[0].acquire()
        
        """set this server in com_arduino"""
        self.com_arduino.set_server_arduino_order(self)
        self.com_arduino.set_server_arduino_order_state(True)
        
        """send all current state : ex pump"""
        self.send_ALL_pump_state()
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
                #print (self.name + " received : "+ data)
                
                data = data.split("\n")
                
                for msg in data : 
                    msg_list = msg.split(":")
                    
                    #print ("daz " +str(volume_cont_list) )
                    try : 
                        if msg_list[0].strip() == "EL" : 
                            if msg_list[3].strip() == "True" : 
                                self._set_EL_received(msg_list[1].strip(), msg_list[2].strip(), True)
                            elif msg_list[3].strip() == "False" : 
                               
                                self._set_EL_received(msg_list[1].strip(), msg_list[2].strip(), False)
                                
                            else : 
                                print ("probleme with EL msg : " + msg) 
                    except Exception : 
                        pass
                    
         
    
    """send all state pump"""
    def send_ALL_pump_state(self): 
        for name in self.current_state._state_pumps :  
            self.current_state.com_arduino.send_server_arduino_order("PUMP", name, self.current_state.get_state_pump(name))
    
    def _answer_EL(self, name_container, name_EL):
        """while no response from the server"""
        self._state_EL_received[0].acquire()
        
        status = self._get_EL_received(name_container, name_EL)
        
        self._state_EL_received[1].release()
        
        return status
    
    def _set_EL_received(self, name_container, name_EL, status):
        
        self._state_EL_received[1].acquire()
        self._state_EL_received[2] = name_container
        self._state_EL_received[3] = name_EL
        self._state_EL_received[4] = status
        self._state_EL_received[0].release()
    
    def _get_EL_received(self, name_container, name_EL):
        status = "NULL"
        
        """update status is it match the EL"""
        if self._state_EL_received[2] == name_container and self._state_EL_received[3] == name_EL : 
            status = self._state_EL_received[4]
        else :
            print ("EL_received does not match EL asked : aksed : " + name_container + "_" + name_EL +"and received " +self._state_EL_received[2]+ "_"+ self._state_EL_received[3] )

        return status
            
    def _send(self , msg):
        self.lock_message.acquire()
        msg = msg + "\n"
        self.client_socket.sendall(msg.encode(encoding='utf_8', errors='strict'))
        self.lock_message.release()
        
    def _recv(self):
        return self.client_socket.recv(1024).decode()   
    
    def stop(self) :
        self.terminated = True
        self._close() 
        self.server.current_state.set_client_connected_state(self.name, False)
        """set the server_arduino_order_state to false"""
        self.com_arduino.set_server_arduino_order_state(False)
        
        print( self.name +" finish")
        
    """set the EL_received with the last EL eceived"""
    

          
    def _close(self):
        self.client_socket.close() 
       
        