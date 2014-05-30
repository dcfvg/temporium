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
        
      
        
        

        
        """def Button"""
        #self.dict()
        
        self.Button_open = tkinter.Button(self,  text ="OPEN", command = self.parent.open_file)        
        self.Button_open.pack()
       
        self.pack(side=LEFT)
        #self.frame_button_state.pack(side = "right",fill=NONE, expand=1)
        
    """rq : a proteger"""
    def display_button(self):
        self.Button_BU1 = tkinter.Button(self,  text ="BU1", command = self.Button_BU1)        
        self.Button_BU1.pack()
        
        self.Button_BU2 = tkinter.Button(self,  text ="BU2", command = self.Button_BU2)        
        self.Button_BU2.pack()
        
        self.Button_BU3 = tkinter.Button(self,  text ="BU3", command = self.Button_BU3)        
        self.Button_BU3.pack()
        
        self.Button_save = tkinter.Button(self,  text ="SAVE", command = self.Button_save)        
        self.Button_save.pack()
        
        self.Button_open.destroy()
            
    def Button_BU1(self) :
        
        self.parent.visual_feedback.current_rect = "BU1"
    def Button_BU2(self) :
        
        self.parent.visual_feedback.current_rect = "BU2"
    def Button_BU3(self) :
        self.parent.visual_feedback.current_rect = "BU3"
    
    def Button_save(self):
        print("SAVING : ")
        file = open("config_crop_BU.txt", "w")
        file.write("Temporium" + "\n")
        file.write("CONFIGURATION_CROP  : BU " + "\n")
        for item in self.parent.visual_feedback.dict_rect : 
            msg = str(self.parent.visual_feedback.dict_rect[item][2]).replace("[","")
            msg = msg.replace("]", "")
            file.write(item + " : " + msg + "\n")
            print(item + " : " + msg)
        file.flush()
        file.close()
        
        
    