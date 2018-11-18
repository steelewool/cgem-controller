# This program is setup to observe Messier objetcs.

# I'm not using the alt/azi to determine if the object is above the horizon
# and I should be.

import spawnSimulator
import convertRaDecToCgemUnits
import cgemInterface
import messierObjectList

if __name__ == '__main__':

    if input("Enter 1 for simulation 2 for hardware ") == 1:
        simulate = True
        print 'Simulate set to true'
    else:
        simulate = False
        print 'Simulate set to false'
        
    sp = spawnSimulator.SpawnSimulator(simulate)
    
    # The initializer for cgemInterface will open the serial port.
    # The default is ./pty1 which works with either the simulator
    # using nullmodem.sh or when using socat. If talking directly
    # to real hardware will want to set port = '/dev/ttyUSB0'
    # or something simular.
    
    cgem       = cgemInterface.CgemInterface()
    convertRa  = convertRaDecToCgemUnits.Ra()
    convertDec = convertRaDecToCgemUnits.Dec()
    
    # messierObjectList goes out to the simbad database and querys
    # for the Messier Objects. It returns a sorted list of those objects
    # ready for observing.
    
    # As of 10/21/18 I was adding the altitude and azimuth of each
    # object in the list.

    messierList = messierObjectList.MessierObjectList()
    
    loopOverAllMessierObjects = True
    while loopOverAllMessierObjects:
        
        # Print the fist object in the list for debugging.    
        # print messierList.objectTable[0].name

        loopOverMessierObjects = True
        index       = 0
        while loopOverMessierObjects:
            x = 0
            if index == len(messierList.objectTable):
                loopOverMessierObjects = False
            else:
                if messierList.objectTable[index].bin() > 0:
                                
                    alt = messierList.objectTable[index].alt.deg
                
                    if alt > 20.0:
                        messierList.objectTable[index].write()
                        azi = messierList.objectTable[index].azi.deg
                
                        print '   alt : ', alt
                        print '   azi : ', azi
                        print

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
                            raFromCgem = convertRa.fromCgem(args[0])
                            decFromCgem = convertDec.fromCgem(args[1])
                            print 'RA  : ', raFromCgem
                            print 'Dec : ', decFromCgem
                            print
                            print
                        elif x == 3:
                            loopOverMessierObjects = False
            index += 1

        print
        print 'Finished the list one time, loop again'
        print

        y = input('1 to loop again, 2 to exit')
        if y == 2:
            loopOverAllMessierObjects = False

        print
        print 'setTime and sort are both being called'
        print
        
        messierList.setTime()
        messierList.sort()

    cgem.quitSimulator() # does nothing when operating with telescope
    cgem.closeSerial()
    sp.shutdown()


    
