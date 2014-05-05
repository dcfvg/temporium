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
        Canvas.__init__(self, parent, width=700, height=800)
        self.parent = parent
        self.pack(side=RIGHT)
        self.update()
        
        self.current_state = current_state
        
        """position and dimension of the elements"""
        self.container_position = {"M1" : [0.02, 0], "M2" : [0.68, 0],\
                                    "BR1" : [0.02, 0.16+0.05],"BR2" : [0.22, 0.16+0.05],"BR3" : [0.42, 0.16+0.05],\
                                    "BU1" : [0.02, 2*(0.16+0.05)],"BU2" : [0.22, 2*(0.16+0.05)],"BU3" : [0.42,2*(0.16+0.05)],\
                                    "AQ" : [0.2, 3*(0.16+0.05)], "S" : [0.2, 4*(0.16+0.05)]}
        
        self.container_dimension = {"M1" : [0.3, 0.16], "M2" : [0.3, 0.16],\
                                    "BR1" : [0.1, 0.16],"BR2" : [0.1, 0.16],"BR3" : [0.1, 0.16],\
                                    "BU1" : [0.1, 0.16],"BU2" : [0.1, 0.16],"BU3" : [0.1, 0.16],\
                                    "AQ" : [0.5, 0.16], "S" : [0.2, 0.16]}
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
                                "P_BU1_AQ" : [[0.02, 3*(0.16 + 0.05) - 0.05/2],self.container_position["BU1"],self.container_position["AQ"]],\
                                "P_BU2_AQ" : [[0.22, 3*(0.16 + 0.05)-0.05/2],self.container_position["BU2"],self.container_position["AQ"]],\
                                "P_BU3_AQ" : [[0.42,  3*(0.16 + 0.05)- 0.05/2],self.container_position["BU3"],self.container_position["AQ"]],\
                                "P_AQ_S" : [[0.2, 4*(0.16+0.05)-0.05/2],self.container_position["AQ"],self.container_position["S"]]}
        

        self.draw()
        self.bind("<Configure>", self.resize)
        
        
        #self.button = tkinter.Button(self,  text ="Hello", command = self.cliquer)
        #self.button.pack(side="right")
        
        
        
    def resize(self, event):
        """called when the user resize the windows, draw the graphics to the new scale"""
        self.draw()       
        
    def draw(self) :
        """draw the graphics, according to the dimensions and positions from the attributs, and from the elements's states from current_state"""
        self.create_rectangle(0,0,self.winfo_width(),self.winfo_height(), fill="white")
         
        """creation of the container """
        for item in self.container_position : 
            self.create_rectangle(self.container_position[item][0]*self.winfo_width(), self.container_position[item][1]*self.winfo_height(),\
                                   (self.container_dimension[item][0] + self.container_position[item][0])*self.winfo_width(), (self.container_dimension[item][1] + self.container_position[item][1])*self.winfo_height(),fill="black"  )
        
        
        """filling of the container """
        for item in self.current_state.occupied_volume : 
            if item == "M1" or item == "M2": 
                self.create_rectangle(self.container_position[item][0]*self.winfo_width(), (self.container_position[item][1]+self.container_dimension[item][1]*(1-self.current_state.occupied_volume[item]))*self.winfo_height(),\
                                   (self.container_dimension[item][0] + self.container_position[item][0])*self.winfo_width(), (self.container_dimension[item][1] + self.container_position[item][1])*self.winfo_height(),fill="white"  )

            else : 

                self.create_rectangle(self.container_position[item][0]*self.winfo_width(), (self.container_position[item][1]+self.container_dimension[item][1]*(1-self.current_state.occupied_volume[item]))*self.winfo_height(),\
                                  (self.container_dimension[item][0] + self.container_position[item][0])*self.winfo_width(), (self.container_dimension[item][1] + self.container_position[item][1])*self.winfo_height(),fill="green"  )
        
        """creation of the pumps"""
        for item in self.pumps_positions : 
            self.create_oval((self.pumps_positions[item][0][0]-0.01)*self.winfo_width(),(self.pumps_positions[item][0][1]-0.01)*self.winfo_height(),(self.pumps_positions[item][0][0]+0.01)*self.winfo_width(),(self.pumps_positions[item][0][1]+0.01)*self.winfo_height(), fill="red")
            """from the container_out to the pump"""
            self.create_line(self.pumps_positions[item][0][0]*self.winfo_width(), self.pumps_positions[item][0][1]*self.winfo_height(), self.pumps_positions[item][1][0]*self.winfo_width(),self.pumps_positions[item][0][1]*self.winfo_height(), fill = "black", dash=(4, 4))
            self.create_line(self.pumps_positions[item][1][0]*self.winfo_width(),self.pumps_positions[item][0][1]*self.winfo_height(), self.pumps_positions[item][1][0]*self.winfo_width(),self.pumps_positions[item][1][1]*self.winfo_height(), fill = "black", dash=(4, 4))
            """from the pump to the container_in"""
            self.create_line(self.pumps_positions[item][0][0]*self.winfo_width(), self.pumps_positions[item][0][1]*self.winfo_height(), self.pumps_positions[item][0][0]*self.winfo_width(),self.pumps_positions[item][2][1]*self.winfo_height(), fill = "black", dash=(4, 4))
            self.create_line(self.pumps_positions[item][0][0]*self.winfo_width(), self.pumps_positions[item][2][1]*self.winfo_height(), self.pumps_positions[item][2][0]*self.winfo_width(),self.pumps_positions[item][2][1]*self.winfo_height(), fill = "black", dash=(4, 4))

            
        for item in self.current_state.state_pumps : 
            if self.current_state.state_pumps[item] :
                self.create_oval((self.pumps_positions[item][0][0]-0.01)*self.winfo_width(),(self.pumps_positions[item][0][1]-0.01)*self.winfo_height(),(self.pumps_positions[item][0][0]+0.01)*self.winfo_width(),(self.pumps_positions[item][0][1]+0.01)*self.winfo_height(), fill="green")
                """from the container_out to the pump"""
                self.create_line(self.pumps_positions[item][0][0]*self.winfo_width(), self.pumps_positions[item][0][1]*self.winfo_height(), self.pumps_positions[item][1][0]*self.winfo_width(),self.pumps_positions[item][0][1]*self.winfo_height(), fill = "green", dash=(4, 4))
                self.create_line(self.pumps_positions[item][1][0]*self.winfo_width(),self.pumps_positions[item][0][1]*self.winfo_height(), self.pumps_positions[item][1][0]*self.winfo_width(),self.pumps_positions[item][1][1]*self.winfo_height(), fill = "green", dash=(4, 4))
                """from the pump to the container_in"""
                self.create_line(self.pumps_positions[item][0][0]*self.winfo_width(), self.pumps_positions[item][0][1]*self.winfo_height(), self.pumps_positions[item][0][0]*self.winfo_width(),self.pumps_positions[item][2][1]*self.winfo_height(), fill = "green", dash=(4, 4))
                self.create_line(self.pumps_positions[item][0][0]*self.winfo_width(), self.pumps_positions[item][2][1]*self.winfo_height(), self.pumps_positions[item][2][0]*self.winfo_width(),self.pumps_positions[item][2][1]*self.winfo_height(), fill = "green", dash=(4, 4))

                
        
        self.update()
    
            
        
        
        """filling of the container"""
        
        

        
        




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
