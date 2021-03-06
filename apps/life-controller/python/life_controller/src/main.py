'''
Created on 9 mai 2014

@author: ensadlab

'''
from GUI.window import *
from current_state import *
from com_arduino import *
from communication.TCP.server import *
from BRBU_controller import *
from seance_controller import *
from BRBU_controller import *
from security_EL import *
from config_manager import *
from current_state_order import *
from aquarium_controller import *
import signal
import sys
from saving_state_thread import *
from time_controller import *


        
        
def handler( signo, sig_frame):
    print("Exiting program")
    cu_state.quit()
    os._exit(0)
    

if __name__ == "__main__":
    
    """test must be set to False when using with terminal mode"""
    test = False
    exposition_bool = False
    AQ_cycle_heavy_bool = False
    for i in sys.argv : 
        if i.strip() == "test" : 
            test = True
            
    
    config_start_file = open("config/config_start.txt", "r")
    # read the ligne one by one
    for ligne in config_start_file:
        #Take out the end symbols (\n)
        ligne = ligne.strip()
        #split on  ":" 
        list = ligne.split(":")
        
        if list[0].strip() == "exposition" :
            exposition_bool = list[1].strip() == "True"
        elif list[0].strip() == "AQ_cycle_heavy" : 
            AQ_cycle_heavy_bool = list[1].strip() == "True"
    
    co_ard = com_arduino(test)
    cu_state = current_state(co_ard)
    co_ard.set_current_state(cu_state)
    co_ard.__readPin__()
    le_server = server('',8000,cu_state)
    BRBU_cont = BRBU_controller(cu_state)
    seance_cont = seance_controller(cu_state)
    aq_controller = aquarium_controller(cu_state)
    config_m = config_manager(cu_state)
    
    cu_state.set_seance_controller(seance_cont)
    cu_state.set_config_manager(config_m)
    cu_state.set_BRBU_controller(BRBU_cont)
    cu_state.set_server(le_server)
    cu_state.set_aquarium_controller(aq_controller)
    
    

    le_server.start()
    BRBU_cont.start()
    s = security_EL(cu_state)
    cu_state.set_security_EL(s)
    
    saving_th = saving_state_thread(cu_state)
    cu_state.set_saving_state_thread(saving_th)
    saving_th.start()
    
    time_cont = time_controller(cu_state)
    time_cont.start()
    """start time_controller"""
    cu_state.set_current_time_controller_state("AQ_cycle_heavy", AQ_cycle_heavy_bool)
    cu_state.set_current_time_controller_state("exposition", exposition_bool)
    
    cu_state.set_security_checking("EL_max", True)
    
    
    for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
            signal.signal(sig,handler)
    
    """will be an option later"""
    GUI = True
    if GUI : 
        current_state_o = current_state_order(cu_state)
        w = window(None, cu_state,current_state_o )
        cu_state.set_windows(w)
        w.title("Temporium : Beta")
        w.mainloop()

    