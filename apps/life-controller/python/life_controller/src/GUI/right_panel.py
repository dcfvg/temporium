'''
Created on Jun 3, 2014

@author: Cactus
'''
import tkinter
from tkinter import *
from GUI.notebook_right import *

class right_panel(Frame):
    '''
    left panel of the GUI
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        Frame.__init__(self, parent)
        self.parent = parent
        
        self.title = Label(self,  text ="ETAT DU TEMPORIUM" ,bg = "white", )
        self.title.pack()
        
        self.notebook_right = notebook_right(self)
        
        
        self.pack(side=RIGHT, fill= BOTH,expand=1)