'''
Created on Jun 3, 2014

@author: Cactus
'''
import tkinter
from tkinter import ttk
from GUI.manual_pump import *
from GUI.manual_action import *
from GUI.cycle_automatique import *

class notebook_left(tkinter.ttk.Notebook):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        tkinter.ttk.Notebook.__init__(self, parent)
        #, width=768, height=576)
        
        self.parent = parent
        self.manual_pump = manual_pump(self)
        self.manual_action = manual_action(self)
        self.cycle_automatique = cycle_automatique(self)

        
        self.add(self.manual_pump, text="Pompes Manuelles")
        self.add(self.manual_action, text="Actions Manuelles")
        self.add(self.cycle_automatique, text= "Cycle Automatique")
        
        self.pack(fill=BOTH, expand=1)
        
        
        
        