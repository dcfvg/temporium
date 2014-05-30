'''
Created on 10 mai 2014

@author: ensadlab
'''
import threading
import os 

class starting_capture(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        thread to start capture 
        '''
        threading.Thread.__init__(self)
        self.nbr = 5
        
    def run(self):
        os.system("bash ~/temporium/apps/capture/capture.sh " + str(self.nbr))
        