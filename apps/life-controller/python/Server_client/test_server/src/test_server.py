'''
Created on Apr 28, 2014

@author: Cactus
'''
import socket 
if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    if server_socket == -1 : 
        print ("Error in socket_server creation ")
    else : 
        print ("Socket_server built")
    
    server_socket.bind(('', 8000))
    server_socket.listen(5)
   
    while True :  
        client_socket, client_address = server_socket.accept()
        print("Client cree")
        
        """Ask connection for a type of client, data is a string"""
        data = client_socket.recv(1024).decode()
        #print(data)
        

