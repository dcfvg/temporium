'''
Created on Apr 28, 2014

@author: Cactus
'''
import socket 
if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    if client_socket == -1 : 
        print ("Error in socket_server creation ")
    else : 
        print ("Socket_server built")
    
    print("connection asked")
    client_socket.connect(('localhost', 8000))
    #client_socket.send(b"daz")
    client_socket.send("daz".encode(encoding='utf_8', errors='strict'))
    
    