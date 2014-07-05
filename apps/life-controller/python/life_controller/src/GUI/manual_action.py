'''
Created on Apr 24, 2014

@author: Cactus
'''
import tkinter
from tkinter import *


class manual_action(Frame):
    
    """Notre fenetre principale.
    Tous les widgets sont stockes comme attributs de cette fenetre."""
    
    def __init__(self, parent):
        Frame.__init__(self, parent, width=768, height=576)
        self.parent = parent
        self.pack(side=LEFT)
        self.current_state_order = self.parent.parent.parent.current_state_order
        self.current_state = self.parent.parent.parent.current_state
        
        """store each button in a dict()like : { "P_M1_BR1" : [0, button, label_state]...}"""
        self.button_biological_actions = {"AQ_filtration" : [0],\
                                "fill_BU1_AQ" : [1],\
                                "fill_BU2_AQ" : [2] ,\
                                "fill_BU3_AQ" : [3],\
                                "empty_BU1_S" : [4],\
                                "empty_BU2_S" : [5],\
                                "empty_BU3_S" : [6],\
                                 }
        
        """current_action_lift_screen"""
        self.button_action_lift_screen = {"lift_down" : [0],\
                                        "lift_up" : [1],\
                                        "screen_down_outside" : [2],\
                                        "screen_up_outside" : [3],\
                                        "screen_down_inside" : [4],\
                                        "screen_up_inside" : [5],\
                                        "lift_down_manual" : [6],\
                                        "lift_up_manual" : [7],\
                                        "screen_down_outside_manual" : [8],\
                                        "screen_up_outside_manual" : [9],\
                                        "screen_down_inside_manual" : [10],\
                                        "screen_up_inside_manual" : [11],\
                                        }

        """current_spectro"""
        self.button_spectro = {"spectro" : [0]}
         
        """current_light_state"""                               
        self.button_light = {"spectro_light" : [0]}
        
        """current_action_evolved"""
        self.button_action_evolved = {"auto_AQ_filtration" : [0],\
                                        "renew_light_AQ_BU1" : [1],\
                                        "renew_light_AQ_BU2" : [2],\
                                        "renew_light_AQ_BU3" : [3],\
                                        "renew_heavy_AQ_BU1" : [4],\
                                        "renew_heavy_AQ_BU2" : [5],\
                                        "renew_heavy_AQ_BU3" : [6],\
                                 }
        
        self.button_current_action_aquarium = {"AQ_emptying_EL_HIGH": [0],\
                                               "AQ_emptying_EL_MIDDLE": [1],\
                                               "AQ_emptying_EL_LOW": [2],\
                                               
                                               }
        
        """list of information asked : name : [lock, state, name_server] """
        self.button_information_asked = {"formation_rate" : [0],\
                                         "level" : [1],\
                                         "level_AQ" : [2],\
                                         "concentration" : [3]}
        
        self.button_current_film_state = {"film" : [0]}
        
        

        self._build_button_biological()
        self._build_button_action_lift_screen()
        self._build_button_spectro()
        self._build_button_light()
        self._build_button_action_evolved()
        self._build_button_information_asked()
        self._build_button_current_film_state()
        """self._build_button_current_action_aquarium()"""
        self._build_state_label()
        self._add_to_frame()
        
        self.pack(side = "left", fill=NONE, expand=1)
    

            
    """build each label state"""
    def _build_state_label(self):
        for item in self.button_biological_actions : 
            self.button_biological_actions[item].append(tkinter.Label(self,bg ='red', text = "FALSE")) 
        for item in self.button_action_lift_screen : 
            self.button_action_lift_screen[item].append(tkinter.Label(self,bg ='red', text = "FALSE")) 
        for item in self.button_spectro : 
            self.button_spectro[item].append(tkinter.Label(self,bg ='red', text = "FALSE"))
        for item in self.button_light : 
            self.button_light[item].append(tkinter.Label(self,bg ='red', text = "FALSE")) 
        for item in self.button_action_evolved : 
            self.button_action_evolved[item].append(tkinter.Label(self,bg ='red', text = "FALSE")) 
        
        for item in self.button_information_asked : 
            self.button_information_asked[item].append(tkinter.Label(self,bg ='red', text = "FALSE")) 
        for item in self.button_current_film_state : 
            self.button_current_film_state[item].append(tkinter.Label(self,bg ='red', text = "FALSE"))  
        for item in self.button_current_film_state : 
            self.button_current_film_state[item].append(tkinter.Label(self,bg ='red', text = "FALSE"))
#         for item in self.button_current_action_aquarium : 
#             self.button_current_action_aquarium[item].append(tkinter.Label(self,bg ='red', text = "FALSE"))
           
              
        
             
            
        
    
    """add the widget to the frame"""
    def _add_to_frame(self):
        """LEFT SIDE"""
        """compting where we are in the grid"""
        compt = 0
        
        Label(self, text = "Biologie : ",fg = "white", bg = "black").grid(sticky = W,row=compt, columnspan = 2)
        compt = compt+1
        
        internal_compt = 0
        for item in self.button_biological_actions :
            internal_compt = internal_compt +1
            self.button_biological_actions[item][1].grid(sticky=W, row= self.button_biological_actions[item][0]+compt, column=0)
            self.button_biological_actions[item][2].grid(sticky=E, row=self.button_biological_actions[item][0]+compt, column=1)
        compt = compt+internal_compt
        
        """#Stockage du des items du dictionnaire button_action_lift_screen pour les stocker dans une liste
                                items_of_button_action_lift_screen = []
                                for item in self.button_action_lift_screen :
                                    print(item)
                                    items_of_button_action_lift_screen = items_of_button_action_lift_screen + [item]
                                print(items_of_button_action_lift_screen)
                                print(items_of_button_action_lift_screen[0:6])"""

        Label(self, text = "Ascenseur : ",fg = "white", bg = "black").grid(sticky = W,row=compt, columnspan = 2)
        compt = compt+1
        
        internal_compt = 0
        for item in self.button_action_lift_screen :
            internal_compt = internal_compt +1
            self.button_action_lift_screen[item][1].grid(sticky=W, row= self.button_action_lift_screen[item][0]+compt, column=0)
            self.button_action_lift_screen[item][2].grid(sticky=E, row=self.button_action_lift_screen[item][0]+compt, column=1)
        compt = compt+internal_compt
        
        """Label(self, text = "Ascenseur Manuel : ",fg = "white", bg = "black").grid(sticky = W,row=compt, columnspan = 2)
                                compt = compt+1"""
        
        """internal_compt = 0
                                for item in items_of_button_action_lift_screen[6:12] :
                                    internal_compt = internal_compt +1
                                    self.button_action_lift_screen[item][1].grid(sticky=W, row= self.button_action_lift_screen[item][0]+compt, column=0)
                                    self.button_action_lift_screen[item][2].grid(sticky=E, row=self.button_action_lift_screen[item][0]+compt, column=1)
                                compt = compt+internal_compt"""
        
        """RIGHT SIDE"""
        """compting where we are in the grid"""
        compt_right = 0

        Label(self, text = "Spectro : ",fg = "white", bg = "black").grid(sticky = W,row=compt_right, column = 2, columnspan = 2)
        compt_right = compt_right+1
        
        internal_compt = 0
        for item in self.button_spectro :
            internal_compt = internal_compt +1
            self.button_spectro[item][1].grid(sticky=W, row= self.button_spectro[item][0]+compt_right, column=2)
            self.button_spectro[item][2].grid(sticky=E, row=self.button_spectro[item][0]+compt_right, column=3)
        compt_right = compt_right+internal_compt
        
        Label(self, text = "Light : ",fg = "white", bg = "black").grid(sticky = W,row=compt_right, column = 2, columnspan = 2)
        compt_right = compt_right+1
        
        internal_compt = 0
        for item in self.button_light :
            internal_compt = internal_compt +1
            self.button_light[item][1].grid(sticky=W, row= self.button_light[item][0]+compt_right, column=2)
            self.button_light[item][2].grid(sticky=E, row=self.button_light[item][0]+compt_right, column=3)
        compt_right = compt_right+internal_compt

        Label(self, text = "Actions evoluees  /!\ BU pas pret /!\ : ",fg = "white", bg = "black").grid(sticky = W,row=compt_right, column = 2, columnspan = 2)
        compt_right = compt_right+1
        
        internal_compt = 0
        for item in self.button_action_evolved :
            internal_compt = internal_compt +1
            self.button_action_evolved[item][1].grid(sticky=W, row= self.button_action_evolved[item][0]+compt_right, column=2)
            self.button_action_evolved[item][2].grid(sticky=E, row=self.button_action_evolved[item][0]+compt_right, column=3)
        compt_right = compt_right+internal_compt
        
        Label(self, text = "Information asked : ",fg = "white", bg = "black").grid(sticky = W,row=compt_right, column = 2, columnspan = 2)
        compt_right = compt_right+1
        
        internal_compt = 0
        for item in self.button_information_asked :
            internal_compt = internal_compt +1
            self.button_information_asked[item][1].grid(sticky=W, row= self.button_information_asked[item][0]+compt_right, column=2)
            self.button_information_asked[item][2].grid(sticky=E, row=self.button_information_asked[item][0]+compt_right, column=3)
        compt_right = compt_right+internal_compt
        
        Label(self, text = "Film : ",fg = "white", bg = "black").grid(sticky = W,row=compt_right, column = 2, columnspan = 2)
        compt_right = compt_right+1
        
        internal_compt = 0
        for item in self.button_current_film_state :
            internal_compt = internal_compt +1
            self.button_current_film_state[item][1].grid(sticky=W, row= self.button_current_film_state[item][0]+compt_right, column=2)
            self.button_current_film_state[item][2].grid(sticky=E, row=self.button_current_film_state[item][0]+compt_right, column=3)
        compt_right = compt_right+internal_compt
        
        """Label(self, text = "Film : ",fg = "white", bg = "black").grid(sticky = W,row=compt_right, column = 2, columnspan = 2)
        compt_right = compt_right+1
        
        internal_compt = 0
        for item in self.button_current_action_aquarium :
            internal_compt = internal_compt +1
            self.button_current_action_aquarium[item][1].grid(sticky=W, row= self.button_current_action_aquarium[item][0]+compt_right, column=2)
            self.button_current_action_aquarium[item][2].grid(sticky=E, row=self.button_current_action_aquarium[item][0]+compt_right, column=3)
        compt_right = compt_right+internal_compt"""
        
        

    """BUILD BUTTON"""
    """build the button associated to the action"""
    def _build_button_biological(self):
        for item in self.button_biological_actions : 
            if item =="AQ_filtration" : 
                self.button_biological_actions[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action("AQ_filtration"))) 
            elif item =="fill_BU1_AQ" : 
                self.button_biological_actions[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action("fill_BU1_AQ")))
            elif item =="fill_BU2_AQ" : 
                self.button_biological_actions[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action("fill_BU2_AQ")))
            elif item =="fill_BU3_AQ" : 
                self.button_biological_actions[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action("fill_BU3_AQ")))
            elif item =="empty_BU1_S" : 
                self.button_biological_actions[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action("empty_BU1_S")))
            elif item =="empty_BU2_S" : 
                self.button_biological_actions[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action("empty_BU2_S")))
            elif item =="empty_BU3_S" : 
                self.button_biological_actions[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action("empty_BU3_S")))
    
    def _build_button_action_lift_screen(self):
        for item in self.button_action_lift_screen : 
            if item =="lift_down" : 
                self.button_action_lift_screen[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action_lift_screen("lift_down"))) 
            elif item =="lift_up" : 
                self.button_action_lift_screen[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action_lift_screen("lift_up")))
            elif item =="screen_down_outside" : 
                self.button_action_lift_screen[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action_lift_screen("screen_down_outside")))
            elif item =="screen_up_outside" : 
                self.button_action_lift_screen[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action_lift_screen("screen_up_outside")))
            elif item =="screen_down_inside" : 
                self.button_action_lift_screen[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action_lift_screen("screen_down_inside")))
            elif item =="screen_up_inside" : 
                self.button_action_lift_screen[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action_lift_screen("screen_up_inside")))
            elif item =="lift_down_manual" : 
                self.button_action_lift_screen[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action_lift_screen("lift_down_manual"))) 
            elif item =="lift_up_manual" : 
                self.button_action_lift_screen[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action_lift_screen("lift_up_manual")))
            elif item =="screen_down_outside_manual" : 
                self.button_action_lift_screen[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action_lift_screen("screen_down_outside_manual")))
            elif item =="screen_up_outside_manual" : 
                self.button_action_lift_screen[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action_lift_screen("screen_up_outside_manual")))
            elif item =="screen_down_inside_manual" : 
                self.button_action_lift_screen[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action_lift_screen("screen_down_inside_manual")))
            elif item =="screen_up_inside_manual" : 
                self.button_action_lift_screen[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action_lift_screen("screen_up_inside_manual")))

    def _build_button_spectro(self):
        for item in self.button_spectro : 
            if item == "spectro" : 
                self.button_spectro[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_spectro("spectro"))) 
    
    def _build_button_light(self):
        for item in self.button_light : 
            if item == "spectro_light" : 
                self.button_light[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_light("spectro_light"))) 
            
    
    def _build_button_action_evolved(self):
        for item in self.button_action_evolved : 
            if item =="auto_AQ_filtration" : 
                self.button_action_evolved[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action_evolved("auto_AQ_filtration"))) 
            elif item =="renew_light_AQ_BU1" : 
                self.button_action_evolved[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action_evolved("renew_light_AQ_BU1")))
            elif item =="renew_light_AQ_BU2" : 
                self.button_action_evolved[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action_evolved("renew_light_AQ_BU2")))
            elif item =="renew_light_AQ_BU3" : 
                self.button_action_evolved[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action_evolved("renew_light_AQ_BU3")))
            elif item =="renew_heavy_AQ_BU1" : 
                self.button_action_evolved[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action_evolved("renew_heavy_AQ_BU1")))
            elif item =="renew_heavy_AQ_BU2" : 
                self.button_action_evolved[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action_evolved("renew_heavy_AQ_BU2")))
            elif item =="renew_heavy_AQ_BU3" : 
                self.button_action_evolved[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_action_evolved("renew_heavy_AQ_BU3")))
    
   
    def _build_button_information_asked(self):
        for item in self.button_information_asked : 
            if item =="formation_rate" : 
                self.button_information_asked[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_information_asked("formation_rate"))) 
            elif item =="level" : 
                self.button_information_asked[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_information_asked("level")))
            elif item =="level_AQ" : 
                self.button_information_asked[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_information_asked("level_AQ")))
            elif item =="concentration" : 
                self.button_information_asked[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_information_asked("concentration")))
           
    def _build_button_current_film_state(self):
        for item in self.button_current_film_state : 
            if item =="film" : 
                self.button_current_film_state[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_current_film_state("film"))) 
    
    """def _build_button_current_action_aquarium(self):
        for item in self.button_current_action_aquarium : 
            if item =="AQ_emptying_EL_HIGH" : 
                self.button_current_action_aquarium[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_current_action_aquarium(item))) 
            elif item =="AQ_emptying_EL_MIDDLE" : 
                self.button_current_action_aquarium[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_current_action_aquarium(item))) 
            elif item =="AQ_emptying_EL_LOW" : 
                self.button_current_action_aquarium[item].append(tkinter.Button(self,  text =item , command = lambda : self.current_state_order.button_current_action_aquarium(item))) 
    """
    
    def refresh_state(self):
        for item in self.button_biological_actions :  
            if self.current_state.get_current_action(item) : 
                color = "green"
                t = "TRUE"
            else : 
                color = "red"
                t = "FALSE"
            self.button_biological_actions[item][2].config (bg = color, text = t)
        
        for item in self.button_action_lift_screen :  
            if self.current_state.get_current_action_lift_screen(item) : 
                color = "green"
                t = "TRUE"
            else : 
                color = "red"
                t = "FALSE"
            self.button_action_lift_screen[item][2].config (bg = color, text = t)
        
        for item in self.button_spectro :  
            if self.current_state.get_current_spectro_state(item) : 
                color = "green"
                t = "TRUE"
            else : 
                color = "red"
                t = "FALSE"
            self.button_spectro[item][2].config (bg = color, text = t)
            
        for item in self.button_light :  
            if self.current_state.get_current_light_state(item) : 
                color = "green"
                t = "TRUE"
            else : 
                color = "red"
                t = "FALSE"
            self.button_light[item][2].config (bg = color, text = t)
        
        for item in self.button_action_evolved :  
            if self.current_state.get_current_action_evolved(item) : 
                color = "green"
                t = "TRUE"
            else : 
                color = "red"
                t = "FALSE"
            self.button_action_evolved[item][2].config (bg = color, text = t)
        
        
        for item in self.button_action_evolved :  
            if self.current_state.get_current_action_evolved(item) : 
                color = "green"
                t = "TRUE"
            else : 
                color = "red"
                t = "FALSE"
            self.button_action_evolved[item][2].config (bg = color, text = t)
        for item in self.button_information_asked :  
            if self.current_state.get_information_asked(item) : 
                color = "green"
                t = "TRUE"
            else : 
                color = "red"
                t = "FALSE"
            self.button_information_asked[item][2].config (bg = color, text = t)
        
        for item in self.button_current_film_state :  
            if self.current_state.get_current_film_state(item) : 
                color = "green"
                t = "TRUE"
            else : 
                color = "red"
                t = "FALSE"
            self.button_current_film_state[item][2].config (bg = color, text = t)
       
        """for item in self.button_current_action_aquarium :  
            if self.current_state.get_current_action_aquarium(item) : 
                color = "green"
                t = "TRUE"
            else : 
                color = "red"
                t = "FALSE"
            self.button_current_action_aquarium[item][2].config (bg = color, text = t)"""
            
        
        
