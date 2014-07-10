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
        
        self.method = StringVar()
        
      
        
        

        
        """def Button"""
        #self.dict()
        
        self.label_choose = Label(self, text = "Choose your method : ",fg = "white", bg = "black")
        self.label_choose.grid(row=0, columnspan = 2)
        self.radio_button_method_manual = tkinter.Radiobutton(self, text="manuelle", variable = self.method, value="manual")
        self.radio_button_method_manual.grid( row = 1, column=0)
        
        self.radio_button_method_autom = tkinter.Radiobutton(self, text="automatique", variable = self.method, value="automatic")
        #self.radio_button_method_autom.pack()
        self.radio_button_method_autom.grid( row = 1, column=1)
        
        self.radio_button_method_autom.select()
        
        self.label_open = Label(self, text = "Open your photo : ",fg = "white", bg = "black")
        self.label_open.grid(row=2, columnspan = 2)
        
        self.Button_open = tkinter.Button(self,  text ="OPEN", command = self.parent.open_file)        
        self.Button_open.grid( row = 3, columnspan = 2)
        #self.Button_open.pack()
        
        
      
       
        self.pack(side=LEFT)
        #self.frame_button_state.pack(side = "right",fill=NONE, expand=1)
        
        """type of detection : LOW or HIGH"""
        self._type_detection = "NULL"
        
    """rq : a proteger"""
    def display_button(self):
        
        self.label_level = Label(self, text = "Choose your level : ",fg = "white", bg = "black")
        self.label_level.grid(row=0, columnspan = 2)
        self.Button_B_HIGH = tkinter.Button(self,  text ="BU HAUT", command = self.Button_B_HIGH)        
        self.Button_B_HIGH.grid(row=1, column = 0)
        
        self.Button_B_LOW = tkinter.Button(self,  text ="BU BAS", command = self.Button_B_LOW)        
        self.Button_B_LOW.grid(row=1, column = 1)
        
        self.label_save = Label(self, text = "Save your level : ",fg = "white", bg = "black")
        self.label_save.grid(row=2, columnspan = 2)
        self.Button_save = tkinter.Button(self,  text ="SAVE", command = self.Button_save)        
        self.Button_save.grid(row=3, columnspan = 2)
        
        """destroying all unused button"""
        self.Button_open.destroy()
        self.label_choose.destroy()
        self.radio_button_method_manual.destroy()
        self.radio_button_method_autom.destroy()
        self.label_open.destroy()
        
        
        
       
            
    def Button_B_HIGH(self) :
        """for each item, calcul the pixel value of the ligne detected"""
        
        if self.method.get() =="automatic" : 
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
        if self.method.get() =="automatic" : 
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
            """file name :  config/config_calibration_BU_LOW.txt"""
            file = open("config/config_calibration_BU_"+self._type_detection+ ".txt", "w")
            
            file.write("Temporium" + "\n")
            file.write("CONFIGURATION_CALIBRATION : BU : "+self._type_detection +  "\n")
            for item in self.parent.visual_feedback.dict_level : 
                msg = str(round(self.parent.visual_feedback.dict_level[item],0))
                
                file.write(item + " : " + self._type_detection + " : " +  msg + "\n")
                print(item + " : " + self._type_detection + " : " +  msg)
            file.flush()
            file.close()
            
        else : 
            print ("Do a detection before saving")
        
        
        
        
    