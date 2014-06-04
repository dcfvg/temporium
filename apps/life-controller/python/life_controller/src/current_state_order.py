'''
Created on Jun 3, 2014

@author: Cactus
'''

class current_state_order(object):
    '''
    objet which bind action from user to an action on the system : to allow the system to be controlled by GUI or network message a same way
    '''


    def __init__(self, a_current_state):
        '''
        Constructor
        '''
        self.current_state = a_current_state
    
    """action corresponding to the pump"""
    def button_pump(self, name):
       
        self.current_state.set_state_pump(name, not self.current_state.get_state_pump(name))
    """action biological"""
    def button_action(self, name):
        self.current_state.set_current_action(name, not self.current_state.get_current_action(name))
    
    """action on the lift system"""
    def button_action_lift_screen(self, name):
        self.current_state.set_current_action_lift_screen(name)
        
    def button_spectro(self, name):
        self.current_state.set_current_spectro_state(name,not self.current_state.get_current_spectro_state(name) )  
    
    def button_light(self, name):
        self.current_state.set_current_light_state(name,not self.current_state.get_current_light_state(name) ) 
    
    def button_BRBU_controller(self, name):
        self.current_state.set_BRBU_controller_state(name,not self.current_state.get_BRBU_controller_state(name) ) 
        
    def button_action_evolved(self, name):
        self.current_state.set_current_action_evolved(name,not self.current_state.get_current_action_evolved(name) ) 
        
    def button_information_asked(self, name):
        self.current_state.set_information_asked(name,not self.current_state.get_information_asked(name) ) 
        
    def button_security_checking(self, name):
        self.current_state.set_security_checking(name,not self.current_state.get_security_checking(name) )
    
    def button_print_ALL_EL(self):
        self.current_state.print_all_EL()
        
    def kill_all(self):
        self.current_state.kill_all()
        
    def Button_P_M1_BR1(self) :
        name = 'P_M1_BR1'
        self.current_state.set_state_pump(name, not self.current_state.get_state_pump(name))
        
    def Button_P_M1_BR2(self) :
        name = 'P_M1_BR2'
        self.current_state.set_state_pump(name, not self.current_state.get_state_pump(name))

        
    def Button_P_M1_BR3(self) :
        name = 'P_M1_BR3'
        self.current_state.set_state_pump(name, not self.current_state.get_state_pump(name))
        
        
    def Button_P_BR1_BU1(self) :
        name = 'P_BR1_BU1'
        self.current_state.set_state_pump(name, not self.current_state.get_state_pump(name))

     
    def Button_P_BR2_BU2(self) :
        name = 'P_BR2_BU2'
        self.current_state.set_state_pump(name, not self.current_state.get_state_pump(name))
        
    def Button_P_BR3_BU3(self) :
        name = 'P_BR3_BU3'
        self.current_state.set_state_pump(name, not self.current_state.get_state_pump(name))
       
    def Button_P_M2_BU1(self) :
        name = 'P_M2_BU1'
        self.current_state.set_state_pump(name, not self.current_state.get_state_pump(name))
     
    def Button_P_M2_BU2(self) :
        name = 'P_M2_BU2'
        self.current_state.set_state_pump(name, not self.current_state.get_state_pump(name))
        
    def Button_P_M2_BU3(self) :
        name = 'P_M2_BU3'
        self.current_state.set_state_pump(name, not self.current_state.get_state_pump(name))
     
    def Button_P_M2_AQ(self):
        name = 'P_M2_AQ'
        self.current_state.set_state_pump(name, not self.current_state.get_state_pump(name))
            
    def Button_P_AQ_S(self):
        name = 'P_AQ_S'
        self.current_state.set_state_pump(name, not self.current_state.get_state_pump(name))
    
    """fake pump"""
    def Button_P_BU1_AQ(self) :
        name = 'fill_BU1_AQ'
        self.current_state.set_current_action(name, not self.current_state.get_current_action(name))
        
    def Button_P_BU2_AQ(self) :
        name = 'fill_BU2_AQ' 
        self.current_state.set_current_action(name, not self.current_state.get_current_action(name))
        
    def Button_P_BU3_AQ(self) :
        name = 'fill_BU3_AQ'
        self.current_state.set_current_action(name, not self.current_state.get_current_action(name))
            
   
        
    def Button_P_BU1_FI(self) :
        name = 'P_BU1_FI'
        
        self.current_state.set_state_pump(name, not self.current_state.get_state_pump(name))
    
    def Button_P_BU2_FI(self) :
        name = 'P_BU2_FI'
        self.current_state.set_state_pump(name, not self.current_state.get_state_pump(name))
    def Button_P_BU3_FI(self) :
        name = 'P_BU3_FI' 
        self.current_state.set_state_pump(name, not self.current_state.get_state_pump(name))
    def Button_P_AQ_FI(self) :
        name = 'P_AQ_FI'

        self.current_state.set_state_pump(name, not self.current_state.get_state_pump(name))
    def Button_P_FI_AQ_1(self) :
        name = 'P_FI_AQ_1'
        self.current_state.set_state_pump(name, not self.current_state.get_state_pump(name))
        
    def Button_P_FI_AQ_3(self) :
        name = 'P_FI_AQ_3'
        self.current_state.set_state_pump(name, not self.current_state.get_state_pump(name))
    
    def Button_P_FI_S(self) :
        name = 'P_FI_S'
        self.current_state.set_state_pump(name, not self.current_state.get_state_pump(name))
        
    def Button_P_SPECTRO(self) :
        name = 'P_SPECTRO'
        self.current_state.set_state_pump(name, not self.current_state.get_state_pump(name)) 
               

    