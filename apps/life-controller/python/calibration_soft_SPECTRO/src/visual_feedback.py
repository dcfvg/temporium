'''
Created on Apr 24, 2014

@author: Cactus
'''


import tkinter as Tk
from tkinter import *
from PIL import Image, ImageTk

"""
 
image = Image.open("lenna.jpg") 
photo = ImageTk.PhotoImage(image) 
 
canvas = Tk.Canvas() 
canvas.create_image(200,500, image=photo)
canvas.pack() """



class visual_feedback(Canvas):
    
    """Notre fenetre principale.
    Tous les widgets sont stockes comme attributs de cette fenetre."""
    
    def __init__(self, parent, file):
        
        self.image = Image.open(file)
        """coeef od reduction for the image"""
        self.image_size_x = self.image.size[0]
        self.image_size_y = self.image.size[1]
        
        """reduction of the image at the beginning"""
        self.reductx = 3
        self.reducty = 3
 

        
        Canvas.__init__(self,bg="black")
        
        self.parent = parent
        self.pack(side=RIGHT, fill=BOTH, expand=True)
        
        self.first = True 

        self.bind("<Configure>", self.resize)
       
        

        """[0,0,0,0] rect in % of the photo"""
        self.dict_rect = self.dict_rect = {"SPECTRO" : [self.create_rectangle(0,0,0,0, outline="red"), [0, 0, 0, 0],"red"]}
        
        """crop values for BU"""
        self.dict_rect_crop = {"SPECTRO" :  [0, 0, 0, 0]}
                               
        
        """values for BU of the absobtion"""
        self.dict_level = {"SPECTRO" :  0}
                               
        
        self.current_rect = "NULL"
        
        self._in_canvas = False
        
    def resize(self, event):
        """if first time, create photo"""
        if self.first :
            im = self.image.resize((int(self.image_size_x/self.reductx),\
                                    int(self.image_size_y/self.reducty)))
            self.config(width=im.size[0], height=im.size[1])
            self.photo = ImageTk.PhotoImage(im)
            self.image_id = self.create_image(0, 0, anchor=NW,  image =self.photo)
            self.read_config_rect()
            self.first = False 
        else :
            #print ("daz")
            self.current_rect = "NULL"
            """called when the user resize the windows, draw the graphics to the new scale"""
            #print ("winfo_height" + str(self.winfo_height()))
            #print ("winfo_width" + str(self.winfo_width()))
            im = self.image.resize((self.winfo_width(),self.winfo_height()))
            self.photo = ImageTk.PhotoImage(im)
            self.delete(self.image_id)
            self.image_id = self.create_image(0, 0, anchor=NW,  image =self.photo)
            for item in self.dict_rect : 
                self.delete(self.dict_rect[item][0])
                self.dict_rect[item][0] = self.create_rectangle(self.dict_rect[item][1][0]*self.winfo_width(),\
                                                                self.dict_rect[item][1][1]*self.winfo_height(),\
                                                                self.dict_rect[item][1][2]*self.winfo_width(),\
                                                                self.dict_rect[item][1][3]*self.winfo_height(),\
                                                                outline=self.dict_rect[item][2])
            
    """refresh without event"""
    def resize_bis(self):
        """if first time, create photo"""
        if self.first :
            im = self.image.resize((int(self.image_size_x/self.reductx),\
                                    int(self.image_size_y/self.reducty)))
            self.config(width=im.size[0], height=im.size[1])
            self.photo = ImageTk.PhotoImage(im)
            self.image_id = self.create_image(0, 0, anchor=NW,  image =self.photo)
            self.read_config_rect()
            self.first = False 
        else :
            #print ("daz")
            self.current_rect = "NULL"
            """called when the user resize the windows, draw the graphics to the new scale"""
            #print ("winfo_height" + str(self.winfo_height()))
            #print ("winfo_width" + str(self.winfo_width()))
            im = self.image.resize((self.winfo_width(),self.winfo_height()))
            self.photo = ImageTk.PhotoImage(im)
            self.delete(self.image_id)
            self.image_id = self.create_image(0, 0, anchor=NW,  image =self.photo)
            for item in self.dict_rect : 
                self.delete(self.dict_rect[item][0])
                self.dict_rect[item][0] = self.create_rectangle(self.dict_rect[item][1][0]*self.winfo_width(),\
                                                                self.dict_rect[item][1][1]*self.winfo_height(),\
                                                                self.dict_rect[item][1][2]*self.winfo_width(),\
                                                                self.dict_rect[item][1][3]*self.winfo_height(),\
                                                                outline=self.dict_rect[item][2])
            
        
    def read_config_rect(self):
        print("read")
        try : 
            file = open("config/config_crop_SPECTRO.txt", "r")
            
    
            for ligne in file :
                """Take out the end symbols (\n)"""
                ligne = ligne.strip()
                """split on  ':' """
                list = ligne.split(":")    
                
                if list[0].strip() == "SPECTRO" :
                    coord = list[1].split(",")
                    """covert in int """
                    coord[0] = int(coord[0].strip())
                    coord[1] = int(coord[1].strip())
                    coord[2] = int(coord[2].strip())
                    coord[3] = int(coord[3].strip())
                    
                    """set in rectangle % """
                    self.dict_rect[list[0].strip()][1][0] = coord[0]/self.image_size_x
                    self.dict_rect[list[0].strip()][1][1] = coord[1]/self.image_size_y
                    self.dict_rect[list[0].strip()][1][2] = coord[2]/self.image_size_x
                    self.dict_rect[list[0].strip()][1][3] = coord[3]/self.image_size_y
                    
                    """set in rectangle pixel for crop """
                    self.dict_rect_crop[list[0].strip()] = coord
                    
            file.close()
            
        except Exception as e : 
            print(str(e))
            print ("no file : config_crop_BU.txt in the directory")
        
    def set_spectro_level(self, name, value):
        """ value of absorbtion""" 
        self.dict_level[name] = value



        
        
        
 
           
    