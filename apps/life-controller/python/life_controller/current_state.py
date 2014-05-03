'''
Created on Apr 27, 2014

@author: Cactus
'''

class current_state(object):
    """ Gather all the informations about the state of the installation"""
    
    def __init__(self):
        """state of each pump : { P_M1_BR1 : True , P_M1_BR2 : False, ...} """
        self.state_pumps = dict()
        self.state_pumps = { "P_M1_BR1" : True , "P_M1_BR2" : True, "P_M1_BR2" : False,\
                             "P_BR1_BU1" : False, "P_BR2_BU2" : False , "P_BR3_BU3" : False,\
                             "P_M2_BU1" : False, "P_M2_BU2" : False , "P_M2_BU3" : False, "P_M2_AQ" : False,\
                             "P_BU1_AQ" : False, "P_BU2_AQ" : False , "P_BU3_AQ" : False,\
                             "P_AQ_S" : False}
        
        """state of each electrode : { EL_M1 : True , EL_M2 : False, ...} """
        self.state_electrodes = dict()
        
        """Occupied volume for each container : { M1 : 0.75 , M2 : ...} """
        self.occupied_volume = dict()
        
        """time of each cycle : { C1 : 75 , C2 : ...}"""
        self.time_cycle = dict()
        
        """Number of usage for each BU : { BU1 : 0 , BU2 : 23, ...} """
        self.number_usage = dict()
        
        self.__setState__()
        
        
    def __setState__(self):
        """ Set the states to the right values according to the log_start.txt file """
            # Open the file
        log_pin = open("log_start.txt", "r")
     
        # read the ligne one by one
        for ligne in log_pin:
            #Take out the end symbols (\n)
            ligne = ligne.strip()
            #split on  ":" 
            list = ligne.split(":")
            
            
            
            if list[0].strip() == "comments" :
                print (list[1].strip())
            
            elif list[0].strip() == "time_cycle" : 
                """set cycle's time { C1 : 75 , C2 : ...} """
                self.time_cycle[list[1].strip()] = float(list[2].strip())
                print ("cycle "+ list[1].strip() +" set at " + list[2].strip())
                
                
            elif list[0].strip() =="occupied_volume" :
                """set the occupied volume { M1 : 0.75 , C2 : ...} """
                self.occupied_volume[list[1].strip()] = float(list[2].strip())
                
            elif list[0].strip() =="number_usage" :
                """set the number_usage { BU1 : 0 , BU2 : 23, ...} """
                self.number_usage[list[1].strip()] = int(list[2].strip())


    
"""
if __name__ == "__main__":
    a = current_state()
    #print(a.the_pins)
"""  
    
    
        
    
