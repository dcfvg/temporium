'''
Created on Jun 3, 2014

@author: Cactus
'''
import tkinter
from tkinter import *
from GUI.notebook_left import *

class left_panel(Frame):
    '''
    left panel of the GUI
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        Frame.__init__(self, parent)
        self.parent = parent
        
        self.title = Label(self,  text ="ACTIONS SUR LE TEMPORIUM" ,bg = "white", )
        self.title.pack()
        
        self.notebook = notebook_left(self)
        
        
        
        
        self.button_kill_all = tkinter.Button(self,  text ="/!\ KILL ALL /!\ " , command = self.parent.current_state_order.kill_all)
        self.button_kill_all.pack()
        
        self.pack(side=LEFT, fill= BOTH,expand=1)
        