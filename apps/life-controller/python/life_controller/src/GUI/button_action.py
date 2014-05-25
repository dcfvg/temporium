'''
Created on Apr 24, 2014

@author: Cactus
'''
import tkinter
from tkinter import *
import time 
from security_EL import *

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
        
        """self.Button_stop = tkinter.Button(self.frame_button,  text ="START/STOP", command = self.stop)        
        self.Button_stop.pack()"""
        
        #self.state_P_M1_BR3 = tkinter.Canvas(self.frame_button_state, bg ='green')
        #self.state_P_M1_BR3.pack()
        
        #self.Button_renew_heavy = tkinter.Button(self.frame_button,  text ="Renouvellement algues lourd", command = self.renew_heavy)        
        #self.Button_renew_heavy.pack()
        #self.state_P_M1_BR3 = tkinter.Canvas(self.frame_button_state, bg ='green')
        #self.state_P_M1_BR3.pack()
        
        self.Button_start_BRBU = tkinter.Button(self.frame_button,  text ="Start BRBU cycle", command = self.start_BRBU_cycle)        
        self.Button_start_BRBU.pack()
        
        self.Button_BRBU_pause = tkinter.Button(self.frame_button,  text ="BRBU_cycle_pause", command = self.BRBU_pause)        
        self.Button_BRBU_pause.pack()
        
        self.Button_lift_down = tkinter.Button(self.frame_button,  text ="lift down", command = self.liftDown)        
        self.Button_lift_down.pack()
        
        
        self.Button_lift_up = tkinter.Button(self.frame_button,  text ="lift up", command = self.liftUp)        
        self.Button_lift_up.pack()
        
        
        self.Button_screen_down = tkinter.Button(self.frame_button,  text ="screen down", command = self.screenDown)        
        self.Button_screen_down.pack()
        
        
        self.Button_screen_up = tkinter.Button(self.frame_button,  text ="screen up", command = self.screenUp)        
        self.Button_screen_up.pack()
        
        self.Button_start_EL = tkinter.Button(self.frame_button,  text ="start_EL", command = self.start_EL)        
        self.Button_start_EL.pack()
        
        self.Button_kill_all = tkinter.Button(self.frame_button,  text ="kill_all", command = self.kill_all)        
        self.Button_kill_all.pack()
        
        self.Button_print_EL = tkinter.Button(self.frame_button,  text ="print EL", command = self.print_EL)        
        self.Button_print_EL.pack()
        
        
        
        """self.Button_refresh = tkinter.Button(self.frame_button,  text ="refresh", command = self.Button_refresh)        
        self.Button_refresh.pack()
        self.state_refresh = tkinter.Canvas(self.frame_button_state, bg ='green')
        self.state_refresh.pack()"""
        
        #self.Button_print = tkinter.Button(self,  text ="print_state", command = self.print_state)        
        #self.Button_print.pack()
        
        
        
        
        #self.button = tkinter.Button(self,  text ="Hello", command = self.cliquer)
        #self.button.pack(side="right")
        
        
        self.bind("<Configure>", self.update())
        
        self.frame_button.pack(side = "left", fill=NONE, expand=1)
        #self.frame_button_state.pack(side = "right",fill=NONE, expand=1)
        
    """rq : a proteger"""
        
    def manual_filtration(self) :
        """check if there is no action running"""
        b = True
        for item in self.current_state._current_action : 
            if not item == "AQ_filtration" :  
                if self.current_state.get_current_action(item) : 
                    b = False
        
        """if there is no action running"""
        if b :  
            self.current_state.set_current_action("AQ_filtration", not self.current_state.get_current_action("AQ_filtration"))

        
    def auto_filtration(self) :
        b = True
        for item in self.current_state._current_action_evolved : 
            if not item == "auto_AQ_filtration" : 
                if self.current_state.get_current_action_evolved(item) : 
                    b = False
        """if there is no action running"""
        if b :
            self.current_state.set_current_action_evolved("auto_AQ_filtration", not self.current_state.get_current_action_evolved("auto_AQ_filtration"))
    
    def renew_light_BU1(self):
        name = "renew_light_AQ_BU1"
        self.current_state.set_current_action_evolved(name,not self.current_state.get_current_action_evolved(name) )
        
    def renew_light_BU2(self):
        name = "renew_light_AQ_BU2"
        self.current_state.set_current_action_evolved(name,not self.current_state.get_current_action_evolved(name) )
        
    def renew_light_BU3(self):
        name = "renew_light_AQ_BU3"
        self.current_state.set_current_action_evolved(name,not self.current_state.get_current_action_evolved(name) )
        
    def renew_heavy(self):
        #renew = renew_aquarium(self.parent.current_state,"heavy")
        pass
    
    def start_BRBU_cycle(self) :
        self.current_state.set_BRBU_controller_state(not self.current_state.get_BRBU_controller_state())
     
    def liftDown(self) :
        self.current_state.com_arduino.liftDown()
           
    def liftUp(self) :
        self.current_state.com_arduino.liftUp()
    
    def screenDown(self) :
        self.current_state.com_arduino.screenDown()
    
    def screenUp(self) :
        self.current_state.com_arduino.screenUp()
        
    def BRBU_pause(self):
        self.current_state.BRBU_controller.pause()
        
    def start_EL(self):
        self.current_state.security_EL.set_stop( not self.current_state.security_EL.get_stop())
        
    def kill_all(self):
        self.current_state.kill_all()
        
    def print_EL(self):
        self.current_state._check_all_EL()
        self.current_state.print_all_EL()
    
    
        
        
        
    
    """def stop(self):
        self.current_state.set_keep_going(not self.current_state.get_keep_going())"""
    
    
                
