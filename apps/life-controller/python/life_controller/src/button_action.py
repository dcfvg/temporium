'''
Created on Apr 24, 2014

@author: Cactus
'''
import tkinter
from tkinter import *
from auto_filtration import *
import time 
from renew_aquarium import *

class button_action(Frame):
    
    """Notre fenetre principale.
    Tous les widgets sont stockes comme attributs de cette fenetre."""
    
    def __init__(self, parent):
        Frame.__init__(self, parent, width=768, height=576)
        self.parent = parent
        self.pack(side=RIGHT)
        

        self.frame_button = Frame(self)
       # self.frame_button_state = Frame(self)
        self.current_state = parent.current_state
        
        

        
        """def Button"""
        #self.dict()
        self.Button_manual_filtration = tkinter.Button(self.frame_button,  text ="Filtration AQ manuelle", command = self.manual_filtration)        
        self.Button_manual_filtration.pack()
        #self.state_P_M1_BR3 = tkinter.Canvas(self.frame_button_state, bg ='green')
        #self.state_P_M1_BR3.pack()
        
        self.Button_auto_filtration = tkinter.Button(self.frame_button,  text ="Filtration Auto 5 min", command = self.auto_filtration)        
        self.Button_auto_filtration.pack()
        #self.state_P_M1_BR3 = tkinter.Canvas(self.frame_button_state, bg ='green')
        #self.state_P_M1_BR3.pack()
        
        #self.Button_cycle_BRBU = tkinter.Button(self.frame_button,  text ="Cycle BRBU", command = self.cycle_BRBU)        
        #self.Button_cycle_BRBU.pack()
        #self.state_P_M1_BR3 = tkinter.Canvas(self.frame_button_state, bg ='green')
        #self.state_P_M1_BR3.pack()
        
        self.Button_renew_light_BU1 = tkinter.Button(self.frame_button,  text ="Renouvellement algues leger BU1", command = self.renew_light_BU1)        
        self.Button_renew_light_BU1.pack()
        #self.state_P_M1_BR3 = tkinter.Canvas(self.frame_button_state, bg ='green')
        #self.state_P_M1_BR3.pack()
        
        self.Button_renew_light_BU2 = tkinter.Button(self.frame_button,  text ="Renouvellement algues leger BU2", command = self.renew_light_BU2)        
        self.Button_renew_light_BU2.pack()
        #self.state_P_M1_BR3 = tkinter.Canvas(self.frame_button_state, bg ='green')
        #self.state_P_M1_BR3.pack()
        
        self.Button_renew_light_BU3 = tkinter.Button(self.frame_button,  text ="Renouvellement algues leger BU3", command = self.renew_light_BU3)        
        self.Button_renew_light_BU3.pack()
        
        #self.state_P_M1_BR3 = tkinter.Canvas(self.frame_button_state, bg ='green')
        #self.state_P_M1_BR3.pack()
        
        #self.Button_renew_heavy = tkinter.Button(self.frame_button,  text ="Renouvellement algues lourd", command = self.renew_heavy)        
        #self.Button_renew_heavy.pack()
        #self.state_P_M1_BR3 = tkinter.Canvas(self.frame_button_state, bg ='green')
        #self.state_P_M1_BR3.pack()
        
        
        
        
        """self.Button_refresh = tkinter.Button(self.frame_button,  text ="refresh", command = self.Button_refresh)        
        self.Button_refresh.pack()
        self.state_refresh = tkinter.Canvas(self.frame_button_state, bg ='green')
        self.state_refresh.pack()"""
        
        #self.Button_print = tkinter.Button(self,  text ="print_state", command = self.print_state)        
        #self.Button_print.pack()
        
        
        
        
        #self.button = tkinter.Button(self,  text ="Hello", command = self.cliquer)
        #self.button.pack(side="right")
        
        
        self.frame_button.pack(side = "left", fill=NONE, expand=1)
        #self.frame_button_state.pack(side = "right",fill=NONE, expand=1)
        
    """rq : a proteger"""
        
    def manual_filtration(self) :
        """check if there is no action running"""
        b = True
        for item in self.current_state._current_action : 
            if not item == "filter_aquarium" :  
                if self.current_state.get_current_action(item) : 
                    b = False
        
        """if there is no action running"""
        if b : 
            self.current_state.filter_aquarium( not self.current_state.get_current_action("filter_aquarium"))

        
    def auto_filtration(self) :
        b = True
        for item in self.current_state._current_action : 
            if self.current_state.get_current_action(item) : 
                b = False
        """if there is no action running"""
        if b : 
            filt = auto_filtration(self.current_state)
            filt.start()
         
    
    def renew_light_BU1(self):
        b = True
        for item in self.current_state._current_action : 
            if self.current_state.get_current_action(item) : 
                b = False
        """if there is no action running"""
        if b : 
            renew = renew_aquarium(self.parent.current_state,"BU1", "light")
            renew.start()
        
    def renew_light_BU2(self):
        b = True
        for item in self.current_state._current_action : 
            if self.current_state.get_current_action(item) : 
                b = False
        """if there is no action running"""
        if b :  
            renew = renew_aquarium(self.parent.current_state,"BU2", "light")
            renew.start()
        
    def renew_light_BU3(self):
        b = True
        for item in self.current_state._current_action : 
            if self.current_state.get_current_action(item) : 
                b = False
        """if there is no action running"""
        if b : 
            renew = renew_aquarium(self.parent.current_state,"BU3","light")
            renew.start()
        
    def renew_heavy(self):
        #renew = renew_aquarium(self.parent.current_state,"heavy")
        pass
    
    def cycle_BRBU(self) :
        pass
    
    
                
