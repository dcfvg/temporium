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
        
        """type of detection : LOW or HIGH"""
        self._type_detection = "NULL"
        
    """rq : a proteger"""
    def display_button(self):
        self.Button_B_HIGH = tkinter.Button(self,  text ="AQ HAUT", command = self.Button_B_HIGH)        
        self.Button_B_HIGH.pack()
        
        self.Button_B_LOW = tkinter.Button(self,  text ="AQ BAS", command = self.Button_B_LOW)        
        self.Button_B_LOW.pack()
        
        self.Button_save = tkinter.Button(self,  text ="SAVE", command = self.Button_save)        
        self.Button_save.pack()
        
        self.Button_open.destroy()
       
            
    def Button_B_HIGH(self) :
        """for each item, calcul the pixel value of the ligne detected"""
        for item in self.parent.visual_feedback.dict_rect_crop : 
            crop = self.parent.visual_feedback.dict_rect_crop[item]
            try : 
                value = int(self.parent.image_level.get_level(self.parent.file, item,  crop))
                self.parent.visual_feedback.set_dec_level(item, value)
            except Exception as e: 
                print (str(e))
                print ("no level detected on " + item )
                value = 0

            print(item + " : " + str(value))
            """set it to visual feedback"""
            
            
        """set the type of detection in order to be able to save"""
        self._type_detection = "HIGH"
        
    def Button_B_LOW(self) :
        """for each item, calcul the pixel value of the ligne detected"""
        for item in self.parent.visual_feedback.dict_rect_crop : 
            crop = self.parent.visual_feedback.dict_rect_crop[item]
            try : 
                value = int(self.parent.image_level.get_level(self.parent.file, item,  crop))
                self.parent.visual_feedback.set_dec_level(item, value)
            except Exception as e: 
                print (str(e))
                print ("no level detected on " + item )
                value = 0
            print(item + " : " + str(value))
            """set it to visual feedback"""
            
            
        """set the type of detection in order to be able to save"""
        self._type_detection = "LOW"
    
    def Button_save(self):
        print("SAVING : ")
        if not self._type_detection == "NULL" :
            """file name :  config/config_calibration_AQ_LOW.txt"""
            file = open("config/config_calibration_AQ_"+self._type_detection+ ".txt", "w")
            
            file.write("Temporium" + "\n")
            file.write("CONFIGURATION_CALIBRATION : AQ : "+self._type_detection +  "\n")
            for item in self.parent.visual_feedback.dict_level : 
                msg = str(self.parent.visual_feedback.dict_level[item])
                
                file.write(item + " : " + self._type_detection + " : " +  msg + "\n")
                print(item + " : " + self._type_detection + " : " +  msg)
            file.flush()
            file.close()
            
        else : 
            print ("Do a detection before saving")
        
        
        
        
    