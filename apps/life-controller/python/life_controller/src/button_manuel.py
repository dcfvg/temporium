'''
Created on Apr 24, 2014

@author: Cactus
'''
import tkinter
from tkinter import *

class button_manuel(Frame):
    
    """Notre fenetre principale.
    Tous les widgets sont stockes comme attributs de cette fenetre."""
    
    def __init__(self, parent):
        Frame.__init__(self, parent, width=768, height=576)
        self.parent = parent
        self.pack(side=LEFT)
        

        self.frame_button = Frame(self)
        self.frame_button_state = Frame(self)
        
        

        
        """def Button"""
        #self.dict()
        self.Button_P_M1_BR1 = tkinter.Button(self.frame_button,  text ="P_M1_BR1", command = self.Button_P_M1_BR1)        
        self.Button_P_M1_BR1.pack()
        self.state_P_M1_BR1 = tkinter.Canvas(self.frame_button_state, bg ='green')
        self.state_P_M1_BR1.pack()
        
        self.Button_P_M1_BR2 = tkinter.Button(self.frame_button,  text ="P_M1_BR2", command = self.Button_P_M1_BR2)        
        self.Button_P_M1_BR2.pack()
        self.state_P_M1_BR2 = tkinter.Canvas(self.frame_button_state, bg ='green')
        self.state_P_M1_BR2.pack()
        
        self.Button_P_M1_BR3 = tkinter.Button(self.frame_button,  text ="P_M1_BR3", command = self.Button_P_M1_BR3)        
        self.Button_P_M1_BR3.pack()
        self.state_P_M1_BR3 = tkinter.Canvas(self.frame_button_state, bg ='green')
        self.state_P_M1_BR3.pack()
        
        self.Button_P_BR1_BU1 = tkinter.Button(self.frame_button,  text ="P_BR1_BU1", command = self.Button_P_BR1_BU1)        
        self.Button_P_BR1_BU1.pack()
        self.state_P_BR1_BU1 = tkinter.Canvas(self.frame_button_state, bg ='green')
        self.state_P_BR1_BU1.pack()
        
        self.Button_P_BR2_BU2 = tkinter.Button(self.frame_button,  text ="P_BR2_BU2", command = self.Button_P_BR2_BU2)        
        self.Button_P_BR2_BU2.pack()
        self.state_P_BR2_BU2 = tkinter.Canvas(self.frame_button_state, bg ='green')
        self.state_P_BR2_BU2.pack()
        
        self.Button_P_BR3_BU3 = tkinter.Button(self.frame_button,  text ="P_BR3_BU3", command = self.Button_P_BR3_BU3)        
        self.Button_P_BR3_BU3.pack()
        self.state_P_BR3_BU3 = tkinter.Canvas(self.frame_button_state, bg ='green')
        self.state_P_BR3_BU3.pack()
        
        self.Button_P_M2_BU1 = tkinter.Button(self.frame_button,  text ="P_M2_BU1", command = self.Button_P_M2_BU1)        
        self.Button_P_M2_BU1.pack()
        self.state_P_M2_BU1 = tkinter.Canvas(self.frame_button_state, bg ='green')
        self.state_P_M2_BU1.pack()
        
        self.Button_P_M2_BU2 = tkinter.Button(self.frame_button,  text ="P_M2_BU2", command = self.Button_P_M2_BU2)        
        self.Button_P_M2_BU2.pack()
        self.state_P_M2_BU2 = tkinter.Canvas(self.frame_button_state, bg ='green')
        self.state_P_M2_BU2.pack()
        
        self.Button_P_M2_BU3 = tkinter.Button(self.frame_button,  text ="P_M2_BU3", command = self.Button_P_M2_BU3)        
        self.Button_P_M2_BU3.pack()
        self.state_P_M2_BU3 = tkinter.Canvas(self.frame_button_state, bg ='green')
        self.state_P_M2_BU3.pack()
        
        self.Button_P_M2_AQ = tkinter.Button(self.frame_button,  text ="P_M2_AQ", command = self.Button_P_M2_AQ)        
        self.Button_P_M2_AQ.pack()
        self.state_P_M2_AQ = tkinter.Canvas(self.frame_button_state, bg ='green')
        self.state_P_M2_AQ.pack()
        
        self.Button_P_BU1_AQ = tkinter.Button(self.frame_button,  text ="P_BU1_AQ", command = self.Button_P_BU1_AQ)        
        self.Button_P_BU1_AQ.pack()
        self.state_P_BU1_AQ = tkinter.Canvas(self.frame_button_state, bg ='green')
        self.state_P_BU1_AQ.pack()
        
        self.Button_P_BU2_AQ = tkinter.Button(self.frame_button,  text ="P_BU2_AQ", command = self.Button_P_BU2_AQ)        
        self.Button_P_BU2_AQ.pack()
        self.state_P_BU2_AQ = tkinter.Canvas(self.frame_button_state, bg ='green')
        self.state_P_BU2_AQ.pack()
        
        self.Button_P_BU3_AQ = tkinter.Button(self.frame_button,  text ="P_BU3_AQ", command = self.Button_P_BU3_AQ)        
        self.Button_P_BU3_AQ.pack()
        self.state_P_BU3_AQ = tkinter.Canvas(self.frame_button_state, bg ='green')
        self.state_P_BU3_AQ.pack()
        
        self.Button_P_AQ_S = tkinter.Button(self.frame_button,  text ="P_AQ_S", command = self.Button_P_AQ_S)        
        self.Button_P_AQ_S.pack()
        self.state_P_AQ_S = tkinter.Canvas(self.frame_button_state, bg ='green')
        self.state_P_AQ_S.pack()
        
        self.Button_refresh = tkinter.Button(self.frame_button,  text ="refresh", command = self.Button_refresh)        
        self.Button_refresh.pack()
        self.state_refresh = tkinter.Canvas(self.frame_button_state, bg ='green')
        self.state_refresh.pack()
        
        #self.Button_print = tkinter.Button(self,  text ="print_state", command = self.print_state)        
        #self.Button_print.pack()
        
        
        
        
        #self.button = tkinter.Button(self,  text ="Hello", command = self.cliquer)
        #self.button.pack(side="right")
        
        
        self.frame_button.pack(side = "left", fill=NONE, expand=1)
        #self.frame_button_state.pack(side = "right",fill=NONE, expand=1)
        
    """rq : a proteger"""
        
    def Button_P_M1_BR1(self) :
        name = 'P_M1_BR1'
        self.parent.current_state.P_M1_BR1(not self.parent.current_state.get_state_pumps(name))
        
    def Button_P_M1_BR2(self) :
        name = 'P_M1_BR2'
        self.parent.current_state.P_M1_BR2(not self.parent.current_state.get_state_pumps(name))

        
    def Button_P_M1_BR3(self) :
        name = 'P_M1_BR3'
        self.parent.current_state.P_M1_BR3(not self.parent.current_state.get_state_pumps(name))
        
        
    def Button_P_BR1_BU1(self) :
        name = 'P_BR1_BU1'
        self.parent.current_state.P_BR1_BU1(not self.parent.current_state.get_state_pumps(name))

     
    def Button_P_BR2_BU2(self) :
        name = 'P_BR2_BU2'
        self.parent.current_state.P_BR2_BU2(not self.parent.current_state.get_state_pumps(name))
        
    def Button_P_BR3_BU3(self) :
        name = 'P_BR3_BU3'
        self.parent.current_state.P_BR3_BU3(not self.parent.current_state.get_state_pumps(name))
        
    def Button_P_BU1_AQ(self) :
        name = 'P_BU1_AQ'
        self.parent.current_state.P_BU1_AQ(not self.parent.current_state.get_state_pumps(name))
        
        
    def Button_P_BU2_AQ(self) :
        name = 'P_BU2_AQ'
        self.parent.current_state.P_BU2_AQ(not self.parent.current_state.get_state_pumps(name))
        
        
    def Button_P_BU3_AQ(self) :
        name = 'P_BU3_AQ'
        self.parent.current_state.P_BU3_AQ(not self.parent.current_state.get_state_pumps(name))
        
       
    def Button_P_M2_BU1(self) :
        name = 'P_M2_BU1'
        self.parent.current_state.P_M2_BU1(not self.parent.current_state.get_state_pumps(name))
     
    def Button_P_M2_BU2(self) :
        name = 'P_M2_BU2'
        self.parent.current_state.P_M2_BU2(not self.parent.current_state.get_state_pumps(name))
        
    def Button_P_M2_BU3(self) :
        name = 'P_M2_BU3'
        self.parent.current_state.P_M2_BU3(not self.parent.current_state.get_state_pumps(name))
     
    def Button_P_M2_AQ(self):
        name = 'P_M2_AQ'
        self.parent.current_state.P_M2_AQ(not self.parent.current_state.get_state_pumps(name))
            
    def Button_P_AQ_S(self):
        name = 'P_AQ_S'
        self.parent.current_state.P_AQ_S(not self.parent.current_state.get_state_pumps(name))
        
    def print_state(self):
        print (self.the_buttons)  
    def Button_refresh(self):
        self.parent.refresh()
        
    
                
