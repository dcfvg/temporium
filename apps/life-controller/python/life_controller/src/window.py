'''
Created on Apr 24, 2014

@author: Cactus
'''
from tkinter import *
from visual_feedback_V2 import *
from visual_feedback import *
from current_state import *
from com_arduino import *
from button_manuel import *
from server import *
import time


class window(Tk):
    '''
    Principal window of the GUI
    '''
    
    

    def __init__(self,parent , current_state):
        '''
        Constructor
        '''
        Tk.__init__(self, parent)
        self.parent = parent
        self.current_state = current_state
        

        self.visual_feedback  = visual_feedback_V2(self, self.current_state)
        self.button_manuel = button_manuel(self)
        
        

    def test_r (self):
        self.refresh()
        self.after_idle(self.test_r)
 

      
    def refresh(self) :
        """Function to call to reresh the GUI"""    
        self.visual_feedback.draw()

        


    
    
    


      
        