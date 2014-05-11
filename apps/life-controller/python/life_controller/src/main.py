'''
Created on 9 mai 2014

@author: ensadlab

'''
from window import *
from current_state import *
from com_arduino import *
from server import *


from BRBU_controller import *

if __name__ == "__main__":
    co_ard = com_arduino()
    cu_state = current_state(co_ard)
    #BRBU_cont = BRBU_controller(cu_state)
    w = window(None, cu_state)
    cu_state.set_windows(w)

    le_server = server('',8000,cu_state)

    le_server.start()
    #BRBU_cont.start()
    
    w.mainloop()

    