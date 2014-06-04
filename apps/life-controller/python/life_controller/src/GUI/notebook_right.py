'''
Created on Jun 3, 2014

@author: Cactus
'''
import tkinter
from tkinter import ttk
from GUI.global_state_frame import *
from GUI.EL_state_frame import *
from GUI.client_connected_frame import *

class notebook_right(tkinter.ttk.Notebook):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        tkinter.ttk.Notebook.__init__(self, parent)
        #, width=768, height=576)
        
        self.parent = parent
        self.global_state_frame = global_state_frame(self)
        self.EL_state_frame = EL_state_frame(self)
        self.client_connected_frame = client_connected_frame(self)

        
        self.add(self.global_state_frame, text="Etat Global")
        self.add(self.EL_state_frame, text="Electrodes")
        self.add(self.client_connected_frame, text="Client connected")
        
        
        self.pack(fill=BOTH, expand=1)
        
        
        
        