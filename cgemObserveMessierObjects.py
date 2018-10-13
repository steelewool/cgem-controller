# This program is setup to observe Messier objetcs.

# I'm not using the alt/azi to determine if the object is above the horizon
# and I should be.

import convertRaDecToCgemUnits
import cgemInterface
import messierObjectList

if __name__ == '__main__':
    
#    cgemInterface = CgemInterface(False)
    
    cgem = cgemInterface.CgemInterface()
#   ra   = convertRaDecToCgemUnits.Ra()
#   dec  = convertRaDecToCgemUnits.Dec()
    
    messierList = messierObjectList.MessierObjectList()
    
    print messierList.objectTable[0].name
    
    loopControl = True
    index = 0
    while loopControl:
        if messierList.objectTable[index].bin() > 0:
            messierList.objectTable[index].write()
            
            x = input('1 to observe, 2 to skip, 3 to exit ')
            if x == 1:
                
                print 'XXX'
                ra = messierList.objectTable[index].ra
                dec = messierList.objectTable[index].dec
            
                print 'YYY'
                
                newRa = convertRaDecToCgemUnits.Ra(float(ra.hr),
                                                   float(ra.min),
                                                   float(ra.sec))

                print 'ZZZ'
            
                newDec = convertRaDecToCgemUnits.Dec(float(dec.deg),
                                                     float(dec.min),
                                                     float(dec.sec))

                print '000'
                
                cgem.gotoCommandWithHP (newRa, newDec)
                print 'result ra/dec: ', cgem.requestHighPrecisionRaDec()
            else:
                if x == 3 or (index == len(messierList.objectTable)-1):
                    loopControl = False
                    
            # print dec.deg, dec_min, deg_sec
#            dec = messierList.objectTable[0].dec
#            cgem.gotoCommand (ra,dec)
#            print messierObjectList.objectTable[0].name

        index += 1

#    cgemInterface.close()
    
