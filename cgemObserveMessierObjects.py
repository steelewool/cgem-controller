# This program is setup to observe Messier objetcs.

# I'm not using the alt/azi to determine if the object is above the horizon
# and I should be.

import convertRaDecToCgemUnits
import cgemInterface
import messierObjectList

if __name__ == '__main__':
    
    # The initializer for cgemInterface will open the serial port.
    # The default is ./pty1 which works with either the simulator
    # using nullmodem.sh or when using socat. If talking directly
    # to real hardware will want to set port = '/dev/ttyUSB0'
    # or something simular.
    
    cgem       = cgemInterface.CgemInterface()
    convertRa  = convertRaDecToCgemUnits.CRa()
    convertDec = convertRaDecToCgemUnits.CDec()
    
    # messierObjectList goes out to the simbad database and querys
    # for the Messier Objects. It returns a sorted list of those objects
    # ready for observing.
    
    # As of 10/21/18 I was adding the altitude and azimuth of each
    # object in the list.
    
    messierList = messierObjectList.MessierObjectList()
    
    # Print the fist object in the list for debugging.
    
    # print messierList.objectTable[0].name

    loopControl = True
    index       = 0
    while loopControl:
        x = 0
        if index == len(messierList.objectTable):
            loopControl = False
        else:
            if messierList.objectTable[index].bin() > 0:
                messierList.objectTable[index].write()
                
                alt = messierList.objectTable[index].alt.deg
                # azi = messierList.objectTable[index].azi.deg
                
                # print 'alt : ', alt
                # print 'azi : ', azi
                
                if alt > 20.0:
                    x = input('1 to observe, 2 to skip, 3 to exit ')
                    if x == 1:
                        
                        ra = messierList.objectTable[index].ra
                        dec = messierList.objectTable[index].dec
                        
                        newRa = convertRaDecToCgemUnits.CRa(float(ra.hr),
                                                            float(ra.min),
                                                            float(ra.sec))
        
                    
                        newDec = convertRaDecToCgemUnits.CDec(float(dec.deg),
                                                              float(dec.min),
                                                              float(dec.sec))
                        
                        cgem.gotoCommandWithHP (newRa, newDec)
                        telescopeRaDecCgem = cgem.requestHighPrecisionRaDec()
                        args = telescopeRaDecCgem.split(',',2)
                        raFromCgem = convertRa.fromCgem(args[0])
                        decFromCgem = convertDec.fromCgem(args[1])
                        print 'RA  : ', raFromCgem
                        print 'Dec : ', decFromCgem
                        print
                        print
                    elif x == 3:
                        loopControl = False
        index += 1

    cgem.quitSimulator() # does nothing when operating with telescope
    cgem.closeSerial()
    
