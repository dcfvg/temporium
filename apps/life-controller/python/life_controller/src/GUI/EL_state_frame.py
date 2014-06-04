'''
Created on Jun 3, 2014

@author: Cactus
'''
import tkinter 
from tkinter import *

class EL_state_frame(Frame):
    '''
    Fra
    '''


    def __init__(self, parent):
        
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack(side=LEFT)
        self.current_state_order = self.parent.parent.parent.current_state_order
        self.current_state = self.parent.parent.parent.current_state
        
        
        """store each button in a dict()like : { "P_M1_BR1" : [0, button, label_state]...}"""
        self.button_biological_actions = {"AQ_filtration" : [0],\
                                "fill_BU1_AQ" : [1],\
                                "fill_BU2_AQ" : [2] ,\
                                "fill_BU3_AQ" : [3],\
                                "empty_BU1_S" : [4],\
                                "empty_BU2_S" : [5],\
                                "empty_BU3_S" : [6],\
                                 }
        
        self.Button_print_EL = tkinter.Button(self,  text ="print EL", command = self.current_state_order.button_print_ALL_EL)        
        self.Button_print_EL.pack()