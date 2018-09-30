# This program is setup to observe Messier objetcs.

# I'm not using the alt/azi to determine if the object is above the horizon
# and I should be.

import convertRaDecToCgemUnits
import cgemInterface
import messierObjectList

if __name__ == '__main__':
    
#    cgemInterface = CgemInterface(False)
    
    cgem = cgemInterface.CgemInterface(False)
#    ra   = convertRaDecToCgemUnits.Ra()
#   dec  = convertRaDecToCgemUnits.Dec()
    
    messierList = messierObjectList.MessierObjectList()
    
    print messierList.objectTable[0].name
    
    loopControl = True
    index = 0
    while loopControl:
#        timeToQuit = input ("Enter a negative 1 to quit ")
#        if timeToQuit == -1:
#            loopControl = False
#        else:
#        print 'binNumber: ', messierList.objectTable[index].bin()
#        print 'index    : ', index
        if messierList.objectTable[index].bin() > 0:
            messierList.objectTable[index].write()
            
            x = input('1 to observe, 2 to skip, 3 to exit ')
            if x == 1:
                ra = messierList.objectTable[index].ra
                dec = messierList.objectTable[index].dec
            
                newRa = convertRaDecToCgemUnits.Ra()
                newRa.hr = float(ra.hr)
                newRa.min = float(ra.min)
                newRa.sec = float(ra.sec)
            
                newDec = convertRaDecToCgemUnits.Dec()
                newDec.deg = float(dec.deg)
                newDec.min = float(dec.min)
                newDec.sec = float(dec.sec)
    
                cgem.gotoCommandWithHP (newRa, newDec)
            else:
                if x == 3 or (index == len(messierList.objectTable)-1):
                    loopControl = False
                    
            # print dec.deg, dec_min, deg_sec
#            dec = messierList.objectTable[0].dec
#            cgem.gotoCommand (ra,dec)
#            print messierObjectList.objectTable[0].name

        index += 1

#    cgemInterface.close()
    