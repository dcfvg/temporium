Settings.ActionLogs=False
Settings.InfoLogs=False
Settings.DebugLogs=False

Settings.MoveMouseDelay = 0 
Settings.DelayAfterDrag = 0
Settings.DelayBeforeDrop = 0
Settings.MoveMouseDelay = 0

EOS=Region(83,25,267,122)

def setLanguage():           # switch to english keyboard
    fr = "finder-drapeaufr.png"; us = Pattern("1348612073658.png").targetOffset(200,0)
    if exists(fr):
        click(fr)
        click(us)
    pass

def focusprocessing():
    #type(Key.TAB,Key.CMD)
    #type(Key.TAB,Key.CMD)
    #
    focuseos()
    wait(.1)
    Region(476,943,315,80).click(Pattern("1392221269693.png").targetOffset(17,2))
    wait(.3)
pass
def focuseos():
    switchApp("EOS Utility")
    pass

def shootandwait():
    
    focusprocessing()         # SCREEN 2 to processing
    
    type("h")                 # flash
    
    click("9.png")            # SCREEN 1 with canon app 
    wait(.4)                  # waiting for camera
    
    focusprocessing()         # SCREEN 2 to processing
    type("g")                 # image
    
    wait(3)                   # time between 2 pictures
    pass

setLanguage()

switchApp("VLC")
focuseos()

for i in range(1,800) :
    shootandwait()

focusprocessing()           # SCREEN 2 to processing
type("k")