'''
Created on Apr 28, 2014

@author: Cactus
'''
import socket
import time 
import threading


class client_arduino_order(threading.Thread):

    def __init__(self, an_adress, a_port, f_analyse_image):
        threading.Thread.__init__(self)
        
        self.name = "client_arduino_order"
        
        self.fake_analyse_image = f_analyse_image
        
        """adress and port to ask connection"""
        self.adress = an_adress
        self.port = a_port
        
        self.connected = False
        self.terminated = False
     
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
                        print (self.name + " received : "+ data)
                        """do whatever you want"""
                        """receive data like "P_M1_BR1 : HIGH"""
                    data = data.split("\n")
                    
                    for item in data : 
                        data_split = item.split(":")
                        try : 
                            if data_split[0].strip() == 'PUMP' :
                                
                                if data_split[2].strip() == 'HIGH' :
                                    self.fake_analyse_image.set_state_pump(data_split[1].strip(), True)
                                
                                elif data_split[2].strip() == 'LOW' : 
                                    self.fake_analyse_image.set_state_pump(data_split[1].strip(), False)
                                else : 
                                    #print("daz1 " + item)
                                    pass
                            
                                """send a answer to the EL aksing"""
                            elif data_split[0].strip() == 'EL' :
                
                                status = self.fake_analyse_image.ask_EL(data_split[1].strip(), data_split[2].strip())
                                self._send(data_split[0].strip() +" : " + data_split[1].strip() +" : " + data_split[2].strip() +" : " + str(status) )
                               
                        except Exception:
                            """Sprint what is wrong"""
                            print(self.name + " Message does not fit the protocol" + item)
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
        self.connected = False
        print(self.name + "finish") 
        
    def stop(self) :
        self.terminated = True
        self._close()
        self.connected = False
        print(self.name + "finish") 
