'''
Created on 9 mai 2014

@author: ensadlab

'''
from GUI.window import *
from current_state import *
from com_arduino import *
from communication.server import *
from BRBU_controller import *
from seance_controller import *
from BRBU_controller import *
from security_EL import *

if __name__ == "__main__":
    co_ard = com_arduino()
    cu_state = current_state(co_ard)
    le_server = server('',8000,cu_state)
    BRBU_cont = BRBU_controller(cu_state)
    w = window(None, cu_state)
    cu_state.set_windows(w)
    cu_state.set_BRBU_controller(BRBU_cont)
    #se = seance_controller(cu_state)
    
    cu_state.set_server(le_server)

    le_server.start()
    BRBU_cont.start()
    s = security_EL(cu_state)
    cu_state.set_security_EL(s)
    
    w.mainloop()

    