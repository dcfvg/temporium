'''
Created on Apr 28, 2014
 
@author: Cactus
'''
import socket
import time
import threading
from image_level import *


 
class client_level_py2(threading.Thread):
 
    def __init__(self):
        threading.Thread.__init__(self)
         
        self.name = "client_level"
         
        self.connected = False
        self.terminated = False

        """Creation of the object image_level"""
         

        self.image_level = image_level(self)

        self.image_level.lock.acquire()

        self.image_level.start()

        """Socket TCP """
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        if self.client_socket == -1 :
            print ("Error in socket_server creation ")
        else :
            print ("Socket_client built")
            """
    def run(self):
        """start to listen"""
        print self.name +" start"
 
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
                    """if order : start, set the order to start giving level information"""



                    if (data =="level_start"):
                        """order to start"""

                        print "Ask for image analysis"
                        self.image_level.lock.release()

                        print "entree dans le Thread"

                       

                        #to complete
                    """if order : stop, set the order to stop giving level information"""
                    if (data =="level_stop"):
                        """order to start"""

                        self.image_level.lock.acquire()

                        

                        #to complete




         
        except IOError:
            print "not ready"
             
             
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
                    print "connection granted"
                    self.start()
                else :
                    print "connection refused"
                    self.stop()
             
            except IOError:
                """Send response message for file not found"""
                print "Pb connection"
                print IOError
        
     
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
        print self.name + "finish"
 
 
if __name__ == "__main__":
    

    client = client_level_py2()
    client.ask_connection('192.168.0.104', 8001)
    #i = input('Choose a number :')



 
     
 
 