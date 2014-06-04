'''
Created on Apr 24, 2014

@author: Cactus
'''
import tkinter
from tkinter import *


class cycle_automatique(Frame):
    
    """Notre fenetre principale.
    Tous les widgets sont stockes comme attributs de cette fenetre."""
    
    def __init__(self, parent):
        Frame.__init__(self, parent, width=768, height=576)
        self.parent = parent
        self.pack(side=LEFT)
        self.current_state_order = self.parent.parent.parent.current_state_order
        self.current_state = self.parent.parent.parent.current_state
        
        """store each button in a dict()like : { "P_M1_BR1" : [0, button, label_state]...}"""
        """BRBU_controller state : true if it is running"""
        self.button_BRBU_controller = {"run" : [0],\
                                       "pause" : [1]}
        
        self.button_security_checking = {"EL_max" : [0]}
        

        self._build_button_BRBU_controller()
        self._build_button_security_checking()
        self._build_state_label()
        self._add_to_frame()
        
        self.pack(side = "left", fill=NONE, expand=1)
    

            
    """build each label state"""
    def _build_state_label(self):
        for item in self.button_BRBU_controller : 
            self.button_BRBU_controller[item].append(tkinter.Label(self,bg ='red', text = "FALSE")) 
        for item in self.button_security_checking : 
            self.button_security_checking[item].append(tkinter.Label(self,bg ='red', text = "FALSE"))  
            
        
        
    
    def _add_to_frame(self):
        """compting where we are in the grid"""
        compt_left = 0
        
        Label(self, text = "Cycle production algues : ",fg = "white", bg = "black").grid(sticky = W,row=compt_left, columnspan = 2)
        compt_left = compt_left+1
        
        internal_compt = 0
        for item in self.button_BRBU_controller :
            internal_compt = internal_compt +1
            self.button_BRBU_controller[item][1].grid(sticky=W, row= self.button_BRBU_controller[item][0]+compt_left, column=0)
            self.button_BRBU_controller[item][2].grid(sticky=E, row=self.button_BRBU_controller[item][0]+compt_left, column=1)
        compt_left = compt_left+internal_compt
        
        Label(self, text = "Security EL checking : ",fg = "white", bg = "black").grid(sticky = W,row=compt_left, columnspan = 2)
        compt_left = compt_left+1
        
        internal_compt = 0
        for item in self.button_security_checking :
            internal_compt = internal_compt +1
            self.button_security_checking[item][1].grid(sticky=W, row= self.button_security_checking[item][0]+compt_left, column=0)
            self.button_security_checking[item][2].grid(sticky=E, row=self.button_security_checking[item][0]+compt_left, column=1)
        compt_left = compt_left+internal_compt
        


    def _build_button_BRBU_controller(self):
        for item in self.button_BRBU_controller : 
            if item =="run" : 
                self.button_BRBU_controller[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_BRBU_controller("run"))) 
            elif item =="pause" : 
                self.button_BRBU_controller[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_BRBU_controller("pause")))
            
    
    def _build_button_security_checking(self):
        for item in self.button_security_checking : 
            if item =="EL_max" : 
                self.button_security_checking[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_security_checking("EL_max"))) 

            
    def refresh_state(self):
        for item in self.button_BRBU_controller :  
            if self.current_state.get_BRBU_controller_state(item) : 
                color = "green"
                t = "TRUE"
            else : 
                color = "red"
                t = "FALSE"
            self.button_BRBU_controller[item][2].config (bg = color, text = t)
            
        for item in self.button_security_checking :  
            if self.current_state.get_security_checking(item) : 
                color = "green"
                t = "TRUE"
            else : 
                color = "red"
                t = "FALSE"
            self.button_security_checking[item][2].config (bg = color, text = t)
   
        
