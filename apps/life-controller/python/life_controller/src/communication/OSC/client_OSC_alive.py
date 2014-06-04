'''
Created on 10 mai 2014

@author: ensadlab
'''
from pythonosc import osc_message_builder
from pythonosc import udp_client

class client_OSC_alive(object):
    '''
    a client OSC that enable to send informationabout the system
    '''


    def __init__(self, ip, port):
        '''
        Create a client UDP with an OSC protocol : send alive signal 
        '''
        self.client = udp_client.UDPClient(ip, port)
    
    """send an alive message : \alive yes"""     
    def send_alive (self):
        
        msg = osc_message_builder.OscMessageBuilder(address = "/alive")
        msg.add_arg("yes")
        msg = msg.build()
        self.client.send(msg)
    
        