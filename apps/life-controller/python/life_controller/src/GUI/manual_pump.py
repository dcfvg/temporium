'''
Created on Apr 24, 2014

@author: Cactus
'''
import tkinter
from tkinter import *


class manual_pump(Frame):
    
    """Notre fenetre principale.
    Tous les widgets sont stockes comme attributs de cette fenetre."""
    
    def __init__(self, parent):
        Frame.__init__(self, parent, width=768, height=576)
        self.parent = parent
        self.pack(side=LEFT)
        self.current_state_order = self.parent.parent.parent.current_state_order
        self.current_state = self.parent.parent.parent.current_state
        
        """store each button in a dict()like : { "P_M1_BR1" : [0, button, label_state]...}"""
        self._button_pumps = { "P_M1_BR1" : [0] , "P_M1_BR2" : [1], "P_M1_BR3" : [2],\
                             "P_BR1_BU1" : [3], "P_BR2_BU2" : [4] , "P_BR3_BU3" : [5],\
                             "P_M2_BU1" : [6], "P_M2_BU2" : [7] , "P_M2_BU3" : [8], "P_M2_AQ" : [9],\
                             "P_SPECTRO" : [10], "P_AQ_S" : [11],\
                             "P_BU1_FI" : [12], "P_BU2_FI" : [13] , "P_BU3_FI" : [14],\
                             "P_AQ_FI" : [15] , "P_FI_AQ_1" : [16], "P_FI_AQ_3" : [17],\
                             "P_FI_S" : [18] }

        self._button_actions = {"AQ_filtration" : [0],\
                                "fill_BU1_AQ" : [1],\
                                "fill_BU2_AQ" : [2] ,\
                                "fill_BU3_AQ" : [3],\
                                "empty_BU1_S" : [4],\
                                "empty_BU2_S" : [5],\
                                "empty_BU3_S" : [6],\
                                 }

        self._build_button_pump()
        self._build_pump_state_label()
        self._add_to_frame()
        
        self.pack(side = "left", fill=NONE, expand=1)
    
    """build each pump button"""
    def _build_button_pump(self):
        for item in self._button_pumps : 
            if item =="P_M1_BR1" : 
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_pump("P_M1_BR1"))) 
            
            elif item =="P_M1_BR2" : 
                
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_pump("P_M1_BR2"))) 
            
            elif item =="P_M1_BR3" : 
                
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_pump("P_M1_BR3"))) 
                
            elif item =="P_BR1_BU1" : 
                
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_pump("P_BR1_BU1"))) 
            
            elif item =="P_BR2_BU2" :
                 
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_pump("P_BR2_BU2"))) 
            
            elif item =="P_BR3_BU3" : 
                
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_pump("P_BR3_BU3"))) 
            
            elif item =="P_M2_BU1" : 
                
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_pump("P_M2_BU1")))
            
            elif item =="P_M2_BU2" : 
                
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_pump("P_M2_BU2")))
            
            elif item =="P_M2_BU3" : 
                
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_pump("P_M2_BU3"))) 
            
            elif item =="P_M2_AQ" : 
                
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_pump("P_M2_AQ"))) 
                
            elif item =="P_BU1_FI" : 
                
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_pump("P_BU1_FI"))) 
            
            elif item =="P_BU2_FI" : 
                
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_pump("P_BU2_FI"))) 
            
            elif item =="P_BU3_FI" : 
                
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_pump("P_BU3_FI"))) 
            
            elif item =="P_AQ_S" :
                 
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_pump("P_AQ_S")))
            
            elif item =="P_AQ_FI" : 
                
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_pump("P_AQ_FI"))) 
            
            elif item =="P_FI_AQ_1" : 
                
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_pump("P_FI_AQ_1"))) 
            
            elif item =="P_FI_AQ_3" : 
                
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_pump("P_FI_AQ_3"))) 
            
            elif item =="P_FI_S" : 
                
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_pump("P_FI_S")))
            
            elif item =="P_SPECTRO" : 
                
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_pump("P_SPECTRO")))
            
    """build each label state"""
    def _build_pump_state_label(self):
        for item in self._button_pumps : 
            self._button_pumps[item].append(tkinter.Label(self,bg ='red', text = "FALSE")) 
    
    
    def _add_to_frame(self):
        Label(self, text = "Pompes : ",fg = "white", bg = "black").grid(sticky = W,row=0, columnspan = 2)
        
        for item in self._button_pumps :
            """if at 9th place, add the warning message of pump whiwh should be used alone"""
            if self._button_pumps[item][0] == 12 :
                Label(self).grid(row=12) 
                Label(self, text = "\n /!\ ATTENTION AVEC CES POMPES /!\ \n",fg="white", bg="black").grid(row=13, columnspan=2)
               
                
              
            if   self._button_pumps[item][0] >= 12 : 
                self._button_pumps[item][0] = self._button_pumps[item][0] +2  
            
            self._button_pumps[item][1].grid(sticky=W, row=self._button_pumps[item][0]+1, column=0)
            self._button_pumps[item][2].grid(sticky=E,row=self._button_pumps[item][0]+1, column=1)
            


    def _build_button_action(self):
        for item in self._button_actions : 
            if item =="AQ_filtration" : 
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action("AQ_filtration"))) 
            elif item =="fill_BU1_AQ" : 
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action("fill_BU1_AQ")))
            elif item =="fill_BU2_AQ" : 
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action("fill_BU2_AQ")))
            elif item =="fill_BU3_AQ" : 
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action("fill_BU3_AQ")))
            elif item =="empty_BU1_S" : 
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action("empty_BU1_S")))
            elif item =="empty_BU2_S" : 
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action("empty_BU2_S")))
            elif item =="empty_BU3_S" : 
                self._button_pumps[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action("empty_BU3_S")))
            
    def refresh_state(self):
        for item in self._button_pumps :  
            if self.current_state.get_state_pump(item) : 
                color = "green"
                t = "TRUE"
            else : 
                color = "red"
                t = "FALSE"
            self._button_pumps[item][2].config (bg = color, text = t)
        
