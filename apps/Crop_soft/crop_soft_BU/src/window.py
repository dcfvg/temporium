'''
Created on Apr 24, 2014

@author: Cactus
'''
from tkinter import *
from visual_feedback import *
from button_manuel import *
import time
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
        
    def open_file(self):
        try : 
            file = filedialog.askopenfilename(parent = self, title="Choisir Image BU")
      
            self.visual_feedback  = visual_feedback(self, file)
            
            self.button_manuel.display_button()
        except Exception: 
            pass
        


        

if __name__ == "__main__":
    
    w = window(None)
    w.mainloop()

    
    
    


      
        