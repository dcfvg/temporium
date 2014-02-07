Settings.ActionLogs=True
Settings.InfoLogs=g
Settings.DebugLogs=True

Settings.MoveMouseDelay = 0 
Settings.DelayAfterDrag = 0
Settings.DelayBeforeDrop = 0
Settings.MoveMouseDelay = 0

def setLanguage():           # switch to english keyboard
    fr = "finder-drapeaufr.png"; us = Pattern("1348612073658.png").targetOffset(200,0)
    if exists(fr):
        click(fr)
        click(us)
    pass

def focusprocessing():
    click(Location(1650,100))
    pass

def shootandwait():
    click(Location(1650,100)) # SCREEN 2 to processing
    type("h")                 # flash 
    # click("9.png")            # SCREEN 1 with canon app 
    wait(.2)                  # waiting for camera
    
    focusprocessing()         # SCREEN 2 to processing
    type("g")                 # image
    
    wait(2)                   # time between 2 pictures
    
    pass

setLanguage()
for i in range(1,10) :
        shootandwait()

focusprocessing()     # SCREEN 2 to processing
type("k")