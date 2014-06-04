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
        
        self.bind("<ButtonPress-1>", self.draw_rect_press)
        self.bind("<B1-Motion>", self.draw_rect)
        self.bind("<Enter>", self.enter)
        self.bind("<Leave>", self.leave)
        self.bind("<Configure>", self.test_resize)
       
        

        
        self.dict_rect = {"BU1" : [self.create_rectangle(0,0,0,0, outline="red"), [0, 0, 0, 0],"red"],\
                          "BU2" : [self.create_rectangle(0,0,0,0, outline="green"),[0, 0, 0, 0],"green"],\
                          "BU3" : [ self.create_rectangle(0,0,0,0, outline="blue"),[0, 0, 0, 0],"blue"]}
        self.current_rect = "NULL"
        
        self._in_canvas = False
        
    def test_resize(self, event):
        if self.first :
            im = self.image.resize((int(self.image_size_x/self.reductx),\
                                    int(self.image_size_y/self.reducty)))
            self.config(width=im.size[0], height=im.size[1])
            self.photo = ImageTk.PhotoImage(im)
            self.image_id = self.create_image(0, 0, anchor=NW,  image =self.photo)
            self.first = False 
        else :
            
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
   
   
    def draw_rect_press(self, event) : 
        #print ("daz" +str((event.x )*self.reductx) + " " + str((event.y )*self.reducty))
        #print ("daz" +str(self.winfo_pointerx()) + " " + str(self.winfo_pointerx()))
        if (not self.current_rect == "NULL") and self._in_canvas :
            self.coords(self.dict_rect[self.current_rect][0],event.x, event.y, event.x,event.y)
            self.dict_rect[self.current_rect][1][0] = event.x/self.winfo_width()
            self.dict_rect[self.current_rect][1][1] = event.y/self.winfo_height()
            self.dict_rect[self.current_rect][1][2] = event.x/self.winfo_width()
            self.dict_rect[self.current_rect][1][3] = event.y/self.winfo_height()
 
    def draw_rect(self, event): 
        
        if (not self.current_rect == "NULL") and self._in_canvas :
            self.dict_rect[self.current_rect][1][2] = event.x/self.winfo_width()
            self.dict_rect[self.current_rect][1][3] = event.y/self.winfo_height()
            self.coords(self.dict_rect[self.current_rect][0],\
                        self.dict_rect[self.current_rect][1][0]*self.winfo_width(),\
                        self.dict_rect[self.current_rect][1][1]*self.winfo_height(),\
                        self.dict_rect[self.current_rect][1][2]*self.winfo_width(),\
                        self.dict_rect[self.current_rect][1][3]*self.winfo_height())
    
    def get_rect_image(self, name):
        coord = [int(self.dict_rect[name][1][0]*self.image_size_x),\
                 int(self.dict_rect[name][1][1]*self.image_size_y),\
                 int(self.dict_rect[name][1][2]*self.image_size_x),\
                 int(self.dict_rect[name][1][3]*self.image_size_y)] 
        return coord
       
    def enter(self, event):
        self._in_canvas = True
      

    def leave(self, event):
        self._in_canvas = False  


        
        
        
 
           
    