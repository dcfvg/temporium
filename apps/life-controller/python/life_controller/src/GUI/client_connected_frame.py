'''
Created on Apr 24, 2014

@author: Cactus
'''
import tkinter
from tkinter import *


class client_connected_frame(Frame):
    
    """Notre fenetre principale.
    Tous les widgets sont stockes comme attributs de cette fenetre."""
    
    def __init__(self, parent):
        Frame.__init__(self, parent, width=768, height=576)
        self.parent = parent
        self.pack(side=LEFT)
        self.current_state_order = self.parent.parent.parent.current_state_order
        self.current_state = self.parent.parent.parent.current_state
        
        """store each button in a dict()like : { "P_M1_BR1" : [0, button, label_state]...}"""
        """list of server in charge of the communication"""
        self.label_client_connected = {"server_formation_rate" : [0],\
                                       "server_level" : [1],\
                                       "server_level_AQ" : [2],\
                                       "server_concentration" : [3],\
                                       "server_arduino_order" : [4]}
        
        
        
        
        

        self._build_label_client_connected()
        self._build_state_label()
        self._add_to_frame()
        
        self.pack(side = "left", fill=NONE, expand=1)
    

            
    """build each label state"""
    def _build_state_label(self):
        for item in self.label_client_connected : 
            self.label_client_connected[item].append(tkinter.Label(self,bg ='red', text = "FALSE")) 
        
            
        
        
    
    def _add_to_frame(self):
        """compting where we are in the grid"""
        compt_right = 0
        
        Label(self, text = "Client connected : ",fg = "white", bg = "black").grid(sticky = W,row=compt_right, columnspan = 2)
        compt_right = compt_right+1
        
        internal_compt = 0
        for item in self.label_client_connected :
            internal_compt = internal_compt +1
            self.label_client_connected[item][1].grid(sticky=W, row= self.label_client_connected[item][0]+compt_right, column=0)
            self.label_client_connected[item][2].grid(sticky=E, row=self.label_client_connected[item][0]+compt_right, column=1)
        compt_right = compt_right+internal_compt
        
        
        
        
    def _build_label_client_connected(self):
        """it's easy for label because no command associated"""
        for item in self.label_client_connected : 
            self.label_client_connected[item].append(tkinter.Label(self,  text =item + " : " ,fg = "black", bg = "white"))
           
            
            
    def refresh_state(self):
        for item in self.label_client_connected :  
            if self.current_state.get_client_connected_state(item) : 
                color = "green"
                t = "TRUE"
            else : 
                color = "red"
                t = "FALSE"
            self.label_client_connected[item][2].config (bg = color, text = t)
        
        