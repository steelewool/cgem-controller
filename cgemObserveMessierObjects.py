# For now this is just a basic test. May want to rename it to something like:
# cgemTest if it actually works.

import convertRaDecToCgemUnits
import cgemInterface
import messierObjectList

if __name__ == '__main__':
    
#    cgemInterface = CgemInterface(False)
    
    cgem = cgemInterface.CgemInterface(False)
    ra   = convertRaDecToCgemUnits.Ra()
    dec  = convertRaDecToCgemUnits.Dec()
    
    print 'Enter a negative number for the RA hours wnd the loop will exit.'

    messierList = messierObjectList.MessierObjectList()
    
    print messierList.objectTable[0].name
    
    loopControl = True
    while loopControl:
        timeToQuit = input ("Enter a negative 1 to quit ")
        if timeToQuit == -1:
            loopControl = False
        else:
            ra = messierList.objectTable[0].write()
#            dec = messierList.objectTable[0].dec
#            cgem.gotoCommand (ra,dec)
#            print messierObjectList.objectTable[0].name

#    cgemInterface.close()
    