'''
Created on 9 mai 2014

@author: ensadlab
'''
from fake_analyse_image import *
from client_level import *

if __name__ == "__main__":
    
    fake = fake_analyse_image()
    client_l = client_level('localhost',8000,fake)
    fake.set_client_level(client_l)

    
    """fake arduino server who give information about the order send to the arduino"""
    
    client_a = client_arduino_order('localhost',8000,fake)
    
    
    fake.start()
    
    a = input("Action to do : 'exit' to quit ").strip()
    if a =="exit" : 
        fake.stop = True
        client_l.stop()
        client_a.stop()