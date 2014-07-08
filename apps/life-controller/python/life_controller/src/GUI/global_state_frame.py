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
        
        """store each button in a dict()like : { "P_M1_BR1" : [0, button, label_state]...}"""
        self._state_EL = {"BR1" : {"MAX" :[0]},\
                          "BR2" : {"MAX" :[1]},\
                          "BR3" : {"MAX" :[2]},\
                          "BU1" : {"MAX" :[3]},\
                          "BU2" : {"MAX" :[4]},\
                          "BU3" : {"MAX" :[5]},\
                          "AQ" : {"MAX" :[6],"HIGH" :[7],"MIDDLE" :[8],"MIN" :[9], }}
        
        self._button_refresh_state_El = {"refresh_EL" : [0]}
                   
                          
        
        self._build_label_BU_state()
        self._build_label_state_EL()
        self._build_button_refresh_state_El()
        self._build_state_label()
        self._add_to_frame()
        
        self.pack(side = "left", fill=NONE, expand=1)
        
    def _build_label_BU_state(self):
        for item in self._BU_state : 
            self._BU_state[item].append(tkinter.Label(self,  text = item + " : ", fg = "black", bg = "white"))
    
    def _build_label_state_EL(self):
        for item in self._state_EL : 
            for item2 in self._state_EL[item] : 
                self._state_EL[item][item2].append(tkinter.Label(self,  text = item + " : ", fg = "black", bg = "white"))
                self._state_EL[item][item2].append(tkinter.Label(self,  text = item2 + " : ", fg = "black", bg = "white"))
    
    def _build_button_refresh_state_El(self):
        for item in self._button_refresh_state_El : 
            if item =="refresh_EL" : 
                self._button_refresh_state_El[item].append(tkinter.Button(self,  text =item , command = self.current_state_order.button_print_ALL_EL)) 
    
    def _build_state_label(self):
        for item in self._BU_state : 
            self._BU_state[item].append(tkinter.Label(self,  text = "NULL" , fg = "black", bg = "white"))
        for item in self._state_EL : 
            for item2 in self._state_EL[item] : 
                self._state_EL[item][item2].append(tkinter.Label(self,  text = "NULL" , fg = "black", bg = "white"))
        
        
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
        
        Label(self, text = "EL STATE : ",fg = "white", bg = "black").grid(sticky = W, row=compt, columnspan = 2)
        compt = compt+1
        
        internal_compt = 0
        for item in self._state_EL : 
            for item2 in self._state_EL[item] : 
                internal_compt = internal_compt +1
                self._state_EL[item][item2][1].grid(sticky=W, row= self._state_EL[item][item2][0]+compt, column=0)
                self._state_EL[item][item2][2].grid(sticky=E, row=self._state_EL[item][item2][0]+compt, column=1)
                self._state_EL[item][item2][3].grid(sticky=E, row=self._state_EL[item][item2][0]+compt, column=2)
                
        compt = compt+internal_compt
        
        internal_compt = 0
        for item in self._button_refresh_state_El : 
            
            internal_compt = internal_compt +1
            self._button_refresh_state_El[item][1].grid(sticky=W, row= self._button_refresh_state_El[item][0]+compt, column=0)
        compt = compt+internal_compt
        
    def refresh_state(self):
        for item in self._BU_state :  
            state = self.current_state.get_BU_state(item)
            self._BU_state[item][2].config (text = state)
        for item in self._state_EL : 
            for item2 in self._state_EL[item] : 
                """Rq : getting state EL but without actually checking them"""
                if self.current_state._get_state_EL(item, item2) == "NULL" :
                    color = "white"
                    t = "NULL"
                    
                elif self.current_state._get_state_EL(item, item2) : 
                    color = "green"
                    t = "TRUE"
                else : 
                    color = "red"
                    t = "FALSE"
                self._state_EL[item][item2][3].config(bg = color, text = t)
   
                
            
                
        
            
            
        #Label(self, text = "Information asked : ",fg = "white", bg = "black").grid(sticky = W,row=compt_right, column = 2, columnspan = 2)
