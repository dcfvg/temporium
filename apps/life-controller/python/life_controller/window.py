'''
Created on Apr 24, 2014

@author: Cactus
'''
from tkinter import *
from visual_feedback import *
from current_state import *
from com_arduino import *
from button_manuel import *

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
        self.visual_feedback = visual_feedback(self, self.current_state)
        self.button_manuel = button_manuel(self)
      
    def refresh(self) :
        """Function to call to reresh the GUI"""    
        self.visual_feedback.draw()   

if __name__ == "__main__":
    co_ard = com_arduino()
    cu_state = current_state(co_ard)
    a = window(None, cu_state)
    cu_state.set_windows(a)
    a.mainloop()
    


      
        