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
        
        """store each button in a dict()like : { "P_M1_BR1" : [0, button, label_state]...}"""
        self._BU_state = {"BU1" : [0],\
                          "BU2" : [1],\
                          "BU3" : [2] }
                          
        
        self._build_label_BU_state()
        self._build_state_label()
        self._add_to_frame()
        
        self.pack(side = "left", fill=NONE, expand=1)
        
    def _build_label_BU_state(self):
        for item in self._BU_state : 
            self._BU_state[item].append(tkinter.Label(self,  text = item + " : ", fg = "black", bg = "white"))
    
    def _build_state_label(self):
        for item in self._BU_state : 
            self._BU_state[item].append(tkinter.Label(self,  text = "NULL" , fg = "black", bg = "white"))
        
    def _add_to_frame(self) :
        compt = 0
        Label(self, text = "BU STATE : ",fg = "white", bg = "black").grid(sticky = W, row=compt, columnspan = 2)
        compt = compt+1
        
        internal_compt = 0
        for item in self._BU_state :
            internal_compt = internal_compt +1
            self._BU_state[item][1].grid(sticky=W, row= self._BU_state[item][0]+compt, column=0)
            self._BU_state[item][2].grid(sticky=E, row=self._BU_state[item][0]+compt, column=1)
        compt = compt+internal_compt
        
    def refresh_state(self):
        for item in self._BU_state :  
            state = self.current_state.get_BU_state(item)
            self._BU_state[item][2].config (text = state)
        
            
            
        #Label(self, text = "Information asked : ",fg = "white", bg = "black").grid(sticky = W,row=compt_right, column = 2, columnspan = 2)
