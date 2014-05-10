'''
Created on 9 mai 2014

@author: ensadlab
'''
import time
import threading

class refresh(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, un_window):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        self.window = un_window

        
    def run(self):
        while True : 

            self.window.after(0,self.window.refresh)
            time.sleep(0.2)
            
        