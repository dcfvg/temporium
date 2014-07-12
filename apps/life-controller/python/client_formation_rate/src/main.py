'''
Created on Jun 4, 2014
1
@author: Cactus
'''
from client_formation_rate import *
import sys 
import signal

def handler( signo, sig_frame):
    print("Exiting program")
    client.stop()
    os._exit(0)
if __name__ == '__main__':

    client = client_formation_rate("localhost", 8000)
    for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
        signal.signal(sig,handler)