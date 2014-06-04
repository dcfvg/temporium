'''
Created on Apr 24, 2014

@author: Cactus
'''
from tkinter import *
from visual_feedback import *
from button_manuel import *
import time
from spectro_level import *
from tkinter import filedialog


class window(Tk):
    '''
    Principal window of the GUI
    '''
    
    

    def __init__(self,parent):
        '''
        Constructor
        '''
        Tk.__init__(self, parent)
        self.parent = parent

        
        self.button_manuel = button_manuel(self)
        self.spectro_level = spectro_level(self)
        
        
    def open_file(self):
        try : 
            self.file = filedialog.askopenfilename(parent = self, title="Choisir Image SPECTRO")
      
            self.visual_feedback  = visual_feedback(self, self.file)
            
            self.button_manuel.display_button()
        except Exception as e: 
            print(str(e))
        




        

if __name__ == "__main__":
    
    w = window(None)
    w.mainloop()

    
    
    


      
        