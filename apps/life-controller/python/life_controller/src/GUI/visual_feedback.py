'''
Created on Apr 24, 2014

@author: Cactus
'''

from tkinter import *
import tkinter



class visual_feedback(Canvas):
    
    """Notre fenetre principale.
    Tous les widgets sont stockes comme attributs de cette fenetre."""
    
    def __init__(self, parent, current_state):
        
        Canvas.__init__(self, parent, width=300, height=500)
        self.parent = parent
        self.pack(side=RIGHT,  fill=NONE, expand=1)
        self.update()
        
        
        self.current_state = current_state
        
        """position and dimension of the elements"""
        self.container_position = {"M1" : [0.02, 0], "M2" : [0.68, 0],\
                                    "BR1" : [0.02, 0.16+0.05],"BR2" : [0.22, 0.16+0.05],"BR3" : [0.42, 0.16+0.05],\
                                    "BU1" : [0.02, 2*(0.16+0.05)],"BU2" : [0.22, 2*(0.16+0.05)],"BU3" : [0.42,2*(0.16+0.05)],\
                                    "AQ" : [0.2, 3*(0.16+0.05)], "S" : [0.2, 4*(0.16+0.05)], "FI" : [0.8, 3*(0.16+0.05)-0.05/2],\
                                    "SPECTRO" : [0.1, 3*(0.16+0.05)+0.16/2]}
        
        self.container_dimension = {"M1" : [0.3, 0.16], "M2" : [0.3, 0.16],\
                                    "BR1" : [0.1, 0.16],"BR2" : [0.1, 0.16],"BR3" : [0.1, 0.16],\
                                    "BU1" : [0.1, 0.16],"BU2" : [0.1, 0.16],"BU3" : [0.1, 0.16],\
                                    "AQ" : [0.5, 0.16], "S" : [0.2, 0.16] , "FI" :[0.3, 0.16],\
                                    "SPECTRO" : [0.05, 0.05]}
        """pumps: {"P_M1_BR1" :[position, position_container_from, position_container_in]"""
        self.pumps_positions = {"P_M1_BR1" : [[0.02, 0.16 + 0.05/2], self.container_position["M1"],self.container_position["BR1"]],\
                                "P_M1_BR2" : [[0.22, 0.16 + 0.05/2], self.container_position["M1"],self.container_position["BR2"]],\
                                "P_M1_BR3" : [[0.42, 0.16 + 0.05/2], self.container_position["M1"],self.container_position["BR3"]],\
                                "P_BR1_BU1" : [[0.02, 2*(0.16 + 0.05) - 0.05/2],self.container_position["BR1"],self.container_position["BU1"]],\
                                "P_BR2_BU2" : [[0.22, 2*(0.16 + 0.05)-0.05/2],self.container_position["BR2"],self.container_position["BU2"]],\
                                "P_BR3_BU3" : [[0.42,  2*(0.16 + 0.05)- 0.05/2],self.container_position["BR3"],self.container_position["BU3"]],\
                                "P_M2_BU1" : [[0.6-0.02, 0.16 + 0.05/2],self.container_position["M2"],self.container_position["BU1"]],\
                                "P_M2_BU2" : [[0.7-0.02,0.16 + 0.05/2],self.container_position["M2"],self.container_position["BU2"]],\
                                "P_M2_BU3" : [[0.8-0.02,0.16 + 0.05/2],self.container_position["M2"],self.container_position["BU3"]],\
                                "P_M2_AQ" : [[0.9-0.02, 0.16 + 0.05/2],self.container_position["M2"],self.container_position["AQ"]],\
                                "P_BU1_FI" : [[0.02, 3*(0.16 + 0.05) - 0.05/2],self.container_position["BU1"],self.container_position["FI"]],\
                                "P_BU2_FI" : [[0.22, 3*(0.16 + 0.05)-0.05/2],self.container_position["BU2"],self.container_position["FI"]],\
                                "P_BU3_FI" : [[0.42,  3*(0.16 + 0.05)- 0.05/2],self.container_position["BU3"],self.container_position["FI"]],\
                                "P_AQ_S" : [[0.2, 4*(0.16+0.05)-0.05/2],self.container_position["AQ"],self.container_position["S"]],\
                                "P_AQ_FI" : [[0.8, 4*(0.16+0.05)-0.05/2],[self.container_position["AQ"][0] +self.container_dimension["AQ"][0], self.container_position["AQ"][1] +self.container_dimension["AQ"][1]] ,[self.container_position["FI"][0],self.container_position["FI"][1]+self.container_dimension["FI"][1] ] ],\
                                "P_FI_AQ_3" : [[0.8, 3*(0.16+0.05)-0.05/2],self.container_position["FI"] ,self.container_position["AQ"]],\
                                "P_FI_AQ_1" : [[0.8, 3*(0.16+0.05)-0.05/4],self.container_position["FI"] ,self.container_position["AQ"]],\
                                "P_FI_S" : [[0.8, 4*(0.16+0.05)-0.05/4],self.container_position["FI"] ,self.container_position["S"]],\
                                "P_SPECTRO" : [[0.1, 3*(0.16+0.05)],self.container_position["AQ"] ,[self.container_position["AQ"][0],self.container_position["AQ"][1] + 0.16] ]}
        
        self.containers = dict()
        self.pumps = dict()

        
        #self.bind("<Configure>", self.resize)
        
        
        
        #self.button = tkinter.Button(self,  text ="Hello", command = self.cliquer)
        #self.button.pack(side="right")
        """draw the graphics, according to the dimensions and positions from the attributs, and from the elements's states from current_state"""
        self.create_rectangle(0,0,self.winfo_width(),self.winfo_height(), fill="white")
 
        
        self.draw_init()
        self.draw()
        
        
    def resize(self, event):
        """called when the user resize the windows, draw the graphics to the new scale"""
        
        """draw the graphics, according to the dimensions and positions from the attributs, and from the elements's states from current_state"""
        self.create_rectangle(0,0,self.winfo_width(),self.winfo_height(), fill="white")
        self.draw_init()
        self.draw()   
        
    def draw(self) :
        """need to be update"""
        #for item in self.current_state._state_pumps : 
        for item in self.pumps_positions : 
            self.set_state_pump(item, self.current_state.get_state_pump(item))
        for item in self.current_state._occupied_volume :
            self.set_fill_container(item, self.current_state.get_occupied_volume(item))
        
        
        
 
           
    def draw_init(self) :
        for item in self.container_dimension: 
            self.containers[item] = self.create_container(item)
        for item in self.pumps_positions : 
            self.pumps[item] = self.create_pump(item)
        
    def create_container(self, item):
        number_container = self.create_rectangle(self.container_position[item][0]*self.winfo_width(), self.container_position[item][1]*self.winfo_height(),\
                                   (self.container_dimension[item][0] + self.container_position[item][0])*self.winfo_width(), (self.container_dimension[item][1] + self.container_position[item][1])*self.winfo_height(),fill="black"  )
        
        if item == "M1" or item == "M2": 
                number_container_filled =  self.create_rectangle(self.container_position[item][0]*self.winfo_width(), (self.container_position[item][1]+self.container_dimension[item][1]*(1-self.current_state.get_occupied_volume(item)))*self.winfo_height(),\
                                   (self.container_dimension[item][0] + self.container_position[item][0])*self.winfo_width(), (self.container_dimension[item][1] + self.container_position[item][1])*self.winfo_height(),fill="white"  )
        
        else : 
            number_container_filled =  self.create_rectangle(self.container_position[item][0]*self.winfo_width(), (self.container_position[item][1]+self.container_dimension[item][1]*(1-self.current_state.get_occupied_volume(item)))*self.winfo_height(),\
                                   (self.container_dimension[item][0] + self.container_position[item][0])*self.winfo_width(), (self.container_dimension[item][1] + self.container_position[item][1])*self.winfo_height(),fill="green"  )
            
        return [number_container, number_container_filled]

    def set_fill_container(self,item, level):
        """hauteur"""
        """getting old coord"""
        box = self.bbox(self.containers[item][0])
        h =  (box[3] - box[1])
        """new coords"""
        y = box[1] + (1-level)*h
        """setting new coords"""
        self.coords(self.containers[item][1],box[0],y,  box[2],box[3])
    
    def create_pump(self, item):
        number_pump = self.create_oval((self.pumps_positions[item][0][0]-0.01)*self.winfo_width(),(self.pumps_positions[item][0][1]-0.01)*self.winfo_height(),(self.pumps_positions[item][0][0]+0.01)*self.winfo_width(),(self.pumps_positions[item][0][1]+0.01)*self.winfo_height(), fill="red")
        
        wires = [self.create_line(self.pumps_positions[item][0][0]*self.winfo_width(), self.pumps_positions[item][0][1]*self.winfo_height(), self.pumps_positions[item][1][0]*self.winfo_width(),self.pumps_positions[item][0][1]*self.winfo_height(), fill = "black"),\
                self.create_line(self.pumps_positions[item][1][0]*self.winfo_width(),self.pumps_positions[item][0][1]*self.winfo_height(), self.pumps_positions[item][1][0]*self.winfo_width(),self.pumps_positions[item][1][1]*self.winfo_height(), fill = "black"),\
            
                self.create_line(self.pumps_positions[item][0][0]*self.winfo_width(), self.pumps_positions[item][0][1]*self.winfo_height(), self.pumps_positions[item][0][0]*self.winfo_width(),self.pumps_positions[item][2][1]*self.winfo_height(), fill = "black"),\
                self.create_line(self.pumps_positions[item][0][0]*self.winfo_width(), self.pumps_positions[item][2][1]*self.winfo_height(), self.pumps_positions[item][2][0]*self.winfo_width(),self.pumps_positions[item][2][1]*self.winfo_height(), fill = "black")]
        
        return [number_pump, wires]
    
    def set_state_pump(self, pump, state):
        if state : 
            self.itemconfig(self.pumps[pump][0], fill="green")
            for i in self.pumps[pump][1]: 
                self.itemconfig(i, fill="green")
        else : 
            self.itemconfig(self.pumps[pump][0], fill="red")
            for i in self.pumps[pump][1]: 
                self.itemconfig(i, fill="red")
        
        



"""
racine= Tk()

zone_dessin = Canvas(racine, width=500, height=500) #Definit les dimensions du canevas
zone_dessin.pack() #Affiche le canevas
zone_dessin.create_line(0,0,500,500) #Dessine une ligne en diagonale
zone_dessin.create_rectangle(100,100,200,200) #dessine un rectangle

bouton_sortir = Button(racine,text="Sortir",command=racine.destroy)

bouton_sortir.pack()

racine.mainloop()
print("daz")
"""
