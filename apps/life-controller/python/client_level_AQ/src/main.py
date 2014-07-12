'''
Created on Jun 4, 2014

@author: Cactus
'''
import sys
import signal
from client_level import *

def handler( signo, sig_frame):
    print("Exiting program")
    client.stop()
    os._exit(0)
    

if __name__ == '__main__':

    client = client_level("localhost", 8000)
    for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
        signal.signal(sig,handler)
