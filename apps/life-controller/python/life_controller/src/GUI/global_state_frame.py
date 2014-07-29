'''
Created on Jun 3, 2014

@author: Cactus
'''
import tkinter
from tkinter import *

class global_state_frame(Frame):
    '''
    Frame wich displays information about the current state of the temporium
    '''


    def __init__(self,parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack(side=LEFT)
        self.current_state_order = self.parent.parent.parent.current_state_order
        self.current_state = self.parent.parent.parent.current_state
        
    