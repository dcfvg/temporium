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
        
        im = Image.open(file)
        """coeef od reduction for the image"""
        self.reductx = 2
        self.reducty = 2
        self.x = int(im.size[0]/self.reductx)
        self.y = int(im.size[1]/self.reducty)
        im = im.resize((self.x,self.y))
        self.photo = ImageTk.PhotoImage(im)
        self.width = im.size[0]
        self.height= im.size[1]
        
        Canvas.__init__(self,bg="black", width=self.width, height=self.height)
        
        self.parent = parent
        self.create_image(0, 0, anchor=NW,  image =self.photo)
        self.pack(side=RIGHT, fill=BOTH, expand=True)
        
        self.bind("<ButtonPress-1>", self.draw_rect_press)
        self.bind("<B1-Motion>", self.draw_rect)
        self.bind("<Enter>", self.enter)
        self.bind("<Leave>", self.leave)
        
        self.update()
        

        #filename = PhotoImage(file = "bitmap.gif")
        #image = canvas.create_image(50, 50, anchor=NE, image=filename)
        
        #self.image = self.create_image(0,0,anchor=NE,image =filename )
        #self.image.pack()
        
        #self.draw()
        self.dict_rect = {"BR1" : [self.create_rectangle(0,0,0,0, outline="red"), [0, 0, 0, 0], [0, 0, 0, 0]],\
                          "BR2" : [self.create_rectangle(0,0,0,0, outline="green"),[0, 0, 0, 0],[0, 0, 0, 0]],\
                          "BR3" : [ self.create_rectangle(0,0,0,0, outline="blue"),[0, 0, 0, 0], [0, 0, 0, 0]]}
        self.current_rect = "NULL"
        
        self._in_canvas = False
        
    def resize(self, event):
        """called when the user resize the windows, draw the graphics to the new scale"""
        pass 
   
    def draw_rect_press(self, event) : 
        #print ("daz" +str((event.x )*self.reductx) + " " + str((event.y )*self.reducty))
        #print ("daz" +str(self.winfo_pointerx()) + " " + str(self.winfo_pointerx()))
        if (not self.current_rect == "NULL") and self._in_canvas :
            self.coords(self.dict_rect[self.current_rect][0],event.x, event.y, event.x,event.y)
            self.dict_rect[self.current_rect][1][0] = event.x
            self.dict_rect[self.current_rect][1][1] = event.y
            self.dict_rect[self.current_rect][1][2] = event.x
            self.dict_rect[self.current_rect][1][3] = event.y 
            self.dict_rect[self.current_rect][2][0] = (event.x )*self.reductx
            self.dict_rect[self.current_rect][2][1] = (event.y )*self.reducty
            self.dict_rect[self.current_rect][2][2] = (event.x )*self.reductx
            self.dict_rect[self.current_rect][2][3] = (event.y )*self.reducty
 
    def draw_rect(self, event): 
        
        if (not self.current_rect == "NULL") and self._in_canvas :
            self.dict_rect[self.current_rect][1][2] = event.x
            self.dict_rect[self.current_rect][1][3] = event.y 
            self.dict_rect[self.current_rect][2][2] = (event.x )*self.reductx
            self.dict_rect[self.current_rect][2][3] = (event.y )*self.reducty
            self.coords(self.dict_rect[self.current_rect][0],self.dict_rect[self.current_rect][1][0], self.dict_rect[self.current_rect][1][1], self.dict_rect[self.current_rect][1][2],self.dict_rect[self.current_rect][1][3])
            
    def enter(self, event):
        self._in_canvas = True
      

    def leave(self, event):
        self._in_canvas = False  


        
        
        
 
           
    