'''
Created on Apr 24, 2014

@author: Cactus
'''
from tkinter import *
from GUI.visual_feedback import *
from GUI.left_panel import *
from GUI.right_panel import *
import time


class window(Tk):
    '''
    Principal window of the GUI
    '''
    
    

    def __init__(self,parent , current_state, a_current_state_order):
        '''
        Constructor
        '''
        Tk.__init__(self, parent)
        self.parent = parent
        
        self.current_state = current_state
        self.current_state_order = a_current_state_order
        
        
        self.right_panel = right_panel( self)
        self.visual_feedback  = visual_feedback(self, self.current_state)
        
        
        self.left_panel = left_panel( self)
        
        
        
        

        
        self.refresh_after()
        
        
    def test_r (self):
        self.refresh()
        self.after_idle(self.test_r)
        
    
    def _redraw(self) :
        """Function to call to reresh the GUI"""    
        self.visual_feedback.draw()
        self.left_panel.notebook.manual_pump.refresh_state()
        self.left_panel.notebook.manual_action.refresh_state()
        self.left_panel.notebook.cycle_automatique.refresh_state()
        self.right_panel.notebook_right.client_connected_frame.refresh_state()
        self.right_panel.notebook_right.global_state_frame.refresh_state()
        #self.right_panel.notebook_right.EL_state_frame.refresh_state()
        
        
        
    
    def refresh_after(self):

        self._redraw()
        self.after(200,self.refresh_after)
        
        #time.sleep(0.1)     
        #self.after_idle(self.refresh_test)


        


    
    
    


      
        