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
        self.Button_SPECTRO = tkinter.Button(self,  text ="AQ", command = self.Button_AQ)        
        self.Button_SPECTRO.pack()
        
        
        self.Button_save = tkinter.Button(self,  text ="SAVE", command = self.Button_save)        
        self.Button_save.pack()
        
        self.Button_open.destroy()
            
    def Button_AQ(self) :
        
        self.parent.visual_feedback.current_rect = "AQ"
    
    
    def Button_save(self):
        print("SAVING : ")
        file = open("config/config_crop_AQ.txt", "w")
        file.write("Temporium" + "\n")
        file.write("CONFIGURATION_CROP  : AQ " + "\n")
        for item in self.parent.visual_feedback.dict_rect : 
            msg = str(self.parent.visual_feedback.get_rect_image(item)).replace("[","")
            msg = msg.replace("]", "")
            file.write(item + " : " + msg + "\n")
            print(item + " : " + msg)
        file.flush()
        file.close()
        
        
    