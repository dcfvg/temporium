'''
Created on Apr 24, 2014

@author: Cactus
'''
from tkinter import *
from visual_feedback import *
from current_state import *

class window(Tk):
    '''
    Principal window of the GUI
    '''
    


    def __init__(self,parent, current_state ):
        '''
        Constructor
        '''
        Tk.__init__(self, parent)
        self.parent = parent
        self.current_state = current_state
        self.visual_feedback = visual_feedback(self, self.current_state)
        

if __name__ == "__main__":
    cu_state = current_state()
    a = window(None, cu_state) 
    a.mainloop()
    


      
        