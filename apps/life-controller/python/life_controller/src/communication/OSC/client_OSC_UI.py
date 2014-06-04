'''
Created on 10 mai 2014

@author: ensadlab
'''
from pythonosc import osc_message_builder
from pythonosc import udp_client

class client_OSC_UI(object):
    '''
    a client OSC that enable to send informationabout the system
    '''


    def __init__(self, un_seance_controller, ip, port):
        '''
        Create a client UDP with an OSC protocol 
        '''
        
        self.seance_controller = un_seance_controller
        
        self.client = udp_client.UDPClient(ip, port)
        
    def xxx (self):

        msg = osc_message_builder.OscMessageBuilder(address = "/xxx")
        msg.add_arg("xxx")
        msg = msg.build()
        self.client.send(msg)
        print("film begin send")
    
 
        