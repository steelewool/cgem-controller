# This program is setup to observe Messier objetcs.

# I'm not using the alt/azi to determine if the object is above the horizon
# and I should be.

import convertRaDecToCgemUnits
import cgemInterface
import messierObjectList

if __name__ == '__main__':
    
    cgem       = cgemInterface.CgemInterface()
    convertRa  = convertRaDecToCgemUnits.Ra()
    convertDec = convertRaDecToCgemUnits.Dec()
    
    messierList = messierObjectList.MessierObjectList()
    
    print messierList.objectTable[0].name
    
    loopControl = True
    index       = 0
    while loopControl:
        x = 0
        if index == len(messierList.objectTable):
            loopControl = False
        else:
            if messierList.objectTable[index].bin() > 0:
                messierList.objectTable[index].write()
                
                x = input('1 to observe, 2 to skip, 3 to exit ')
                if x == 1:
                    
                    ra = messierList.objectTable[index].ra
                    dec = messierList.objectTable[index].dec
                    
                    newRa = convertRaDecToCgemUnits.Ra(float(ra.hr),
                                                       float(ra.min),
                                                       float(ra.sec))
    
                
                    newDec = convertRaDecToCgemUnits.Dec(float(dec.deg),
                                                         float(dec.min),
                                                         float(dec.sec))
                    
                    cgem.gotoCommandWithHP (newRa, newDec)
                    telescopeRaDecCgem = cgem.requestHighPrecisionRaDec()
                    args = telescopeRaDecCgem.split(',',2)
                    ra = convertRa.fromCgem(args[0])
                    dec = convertDec.fromCgem(args[1])
                    print 'RA  : ', ra
                    print 'Dec : ', dec
                    print
                    print
                elif x == 3:
                    loopControl = False
        index += 1

    cgem.quitSimulator() # does nothing when operating with telescope
    cgem.closeSerial()
    
