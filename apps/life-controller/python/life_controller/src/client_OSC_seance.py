'''
Created on 10 mai 2014

@author: ensadlab
'''
from pythonosc import osc_message_builder
from pythonosc import udp_client

class client_OSC_seance(object):
    '''
    a client OSC that enable to send order to the film_controller
    '''


    def __init__(self, un_seance_controller, ip, port):
        '''
        Create a client UDP with an OSC protocol 
        '''
        
        self.seance_controller = un_seance_controller
        
        self.client = udp_client.UDPClient(ip, port)
        
    def send_seance_begin (self):
        """order are :   
            - debut seance : /seance, begin """
        msg = osc_message_builder.OscMessageBuilder(address = "/seance_start")
        msg.add_arg("begin")
        msg = msg.build()
        self.client.send(msg)
        print("film begin send")
    
    def send_seance_image_formation (self, value):
        """order are :   
            - rate of image_foramtion : /image_formation, value """
        msg = osc_message_builder.OscMessageBuilder(address = "/image_formation")
        msg.add_arg(value)
        msg = msg.build()
        self.client.send(msg)
        