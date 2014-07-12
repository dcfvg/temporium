'''
Created on Jun 4, 2014

@author: Cactus
'''
from client_spectro import *
import sys
import signal

def handler( signo, sig_frame):
    print("Exiting program")
    client.stop()
    os._exit(0)

if __name__ == '__main__':

    
    for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
        signal.signal(sig,handler)
        
    client = client_spectro("localhost", 8000)
    