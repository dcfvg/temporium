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
    
    def __init__(self, parent, file, method):
        
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
        self.dict_rect = {"BR1" : [self.create_rectangle(0,0,0,0, outline="red"), [0, 0, 0, 0],"red"],\
                          "BR2" : [self.create_rectangle(0,0,0,0, outline="green"),[0, 0, 0, 0],"green"],\
                          "BR3" : [ self.create_rectangle(0,0,0,0, outline="blue"),[0, 0, 0, 0], "blue"]}
        
        """crop values for BR"""
        self.dict_rect_crop = {"BR1" :  [0, 0, 0, 0],\
                               "BR2" :  [0, 0, 0, 0],\
                               "BR3" :  [0, 0, 0, 0]}
        
        """crop values for BR : pixel value in cropped image"""
        self.dict_level = {"BR1" :  0,\
                               "BR2" :  0,\
                               "BR3" :  0}
        
        """line for showing level"""
        self.dict_line_level = {"BR1" :  [0, [0,0,0,0],self.create_line(0,0,0,0, fill="white")],\
                               "BR2" :  [0, [0,0,0,0],self.create_line(0,0,0,0, fill="white")],\
                               "BR3" :  [0, [0,0,0,0],self.create_line(0,0,0,0, fill="white")]}
        
        self.current_rect = "NULL"
        
        self._in_canvas = False
        
        if method =="manual" :
            self.bind("<ButtonPress-1>", self.draw_line_press)
            self.bind("<B1-Motion>", self.draw_line)
            self.bind("<Enter>", self.enter)
            self.bind("<Leave>", self.leave)
        
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
            for item in self.dict_line_level : 
                """delete ol line"""
                self.delete(self.dict_line_level[item][2])
                """create new line"""
                self.dict_line_level[item][2] = self.create_line(self.dict_line_level[item][1][0]*self.winfo_width(),\
                                                                 self.dict_line_level[item][1][1]*self.winfo_height(),\
                                                                 self.dict_line_level[item][1][2]*self.winfo_width(),\
                                                                 self.dict_line_level[item][1][3]*self.winfo_height(),\
                                                                 fill = "white")
                
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
            #self.current_rect = "NULL"
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
            for item in self.dict_line_level : 
                """delete ol line"""
                self.delete(self.dict_line_level[item][2])
                """create new line"""
                self.dict_line_level[item][2] = self.create_line(self.dict_line_level[item][1][0]*self.winfo_width(),\
                                                                 self.dict_line_level[item][1][1]*self.winfo_height(),\
                                                                 self.dict_line_level[item][1][2]*self.winfo_width(),\
                                                                 self.dict_line_level[item][1][3]*self.winfo_height(),\
                                                                 fill = "white")
    
    def get_rect_image(self, name):
        coord = [int(self.dict_rect[name][1][0]*self.image_size_x),\
                 int(self.dict_rect[name][1][1]*self.image_size_y),\
                 int(self.dict_rect[name][1][2]*self.image_size_x),\
                 int(self.dict_rect[name][1][3]*self.image_size_y)] 
        return coord
    
    """teake the name of the container, the pixel value in the ropped image"""
    def set_dec_level(self, name, value):
        """pixel value in cropped image""" 
        self.dict_level[name] = value
        """% value in the whole image"""
        self.dict_line_level[name][0] = (self.dict_rect_crop[name][1] + value)/self.image_size_y
        
        """% of the line to create"""
        self.dict_line_level[name][1] = [self.dict_rect[name][1][0],\
                                         self.dict_line_level[name][0],\
                                         self.dict_rect[name][1][2],\
                                         self.dict_line_level[name][0]]
        
        """refresh GUI"""
        self.resize_bis()
        
    def read_config_rect(self):
        print("read")
        try : 
            file = open("config/config_crop_BR.txt", "r")
            
    
            for ligne in file :
                """Take out the end symbols (\n)"""
                ligne = ligne.strip()
                """split on  ':' """
                list = ligne.split(":")    
                
                if list[0].strip() == "BR1" :
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
                    
                elif list[0].strip() == "BR2" :
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
                    
                elif list[0].strip() == "BR3" :
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
        
        except Exception as e : 
            print(str(e))
            print ("no file : config_crop_BR.txt in the directory")
        
    def enter(self, event):
        self._in_canvas = True
      

    def leave(self, event):
        self._in_canvas = False  

    """return the name of the container where the pointer is"""
    def get_in_container(self, percent_x, percent_y):
        name_container = "NULL"
        for item in self.dict_rect : 
            if percent_x > self.dict_rect[item][1][0] and\
               percent_x <self.dict_rect[item][1][2] and\
               percent_y > self.dict_rect[item][1][1] and\
               percent_y < self.dict_rect[item][1][3] : 
               
                name_container = item
        return name_container
            
               

    def draw_line_press(self, event):
        
        if not self.parent.button_manuel._type_detection == "NULL" :
            name_container = self.get_in_container(event.x/self.winfo_width(), event.y/self.winfo_height())
            self.current_rect = name_container 
            
            if not self.current_rect == "NULL" : 
                
                """geting pixel value in the cropped image"""
                value = int((event.y / self.winfo_height())*self.image_size_y - self.dict_rect_crop[self.current_rect][1] )
                self.set_dec_level(self.current_rect, value )
            
        
    def draw_line(self, event):
        if not self.parent.button_manuel._type_detection == "NULL" :
            self.current_rect = self.get_in_container(event.x/self.winfo_width(), event.y/self.winfo_height())
            if not self.current_rect == "NULL" :
                 
                """geting pixel value in the cropped image"""
                value = int((event.y / self.winfo_height())*self.image_size_y - self.dict_rect_crop[self.current_rect][1]) 
                self.set_dec_level(self.current_rect, value )
            
              
    