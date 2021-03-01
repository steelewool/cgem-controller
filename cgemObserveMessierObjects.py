# This program is setup to observe Messier objetcs.

# I'm not using the alt/azi to determine if the object is above the horizon
# and I should be.

# Version working on the telescope
# commit e51ecdc9a67699133f19de118f314c9fc5237605

import spawnSimulator
import convertRaDecToCgemUnits
import cgemInterface
import messierObjectList

if __name__ == '__main__':

    # Request input as to if simulation or using telescope hardware
    
    if input("Enter 1 for simulation 2 for hardware ") == '1':
        simulate = True
    else:
        simulate = False
    
    # This will either spawn a shell program for setting up the
    # ports for a simulator or for debugging and talking to the
    # telescope. The name is deceiving - but it required.

    sp = spawnSimulator.SpawnSimulator(simulate)
    
    # The initializer for cgemInterface will open the serial port.
    # The default is ./pty1 which works with either the simulator
    # using nullmodem.sh or when using socat. If talking directly
    # to real hardware will want to set port = '/dev/ttyUSB0'
    # or something simular.

    cgem       = cgemInterface.CgemInterface()

    convertRa  = convertRaDecToCgemUnits.ConvertRa()
    convertDec = convertRaDecToCgemUnits.ConvertDec()
    
    # messierObjectList goes out to the simbad database and querys
    # for the Messier Objects. It returns a sorted list of those objects
    # ready for observing.
    
    # As of 10/21/18 I was adding the altitude and azimuth of each
    # object in the list.

    messierList = messierObjectList.MessierObjectList()

    print ('Loop over all messier objects.')
    
    loopOverAllMessierObjects = True
    while loopOverAllMessierObjects:
        
        # Print the fist object in the list for debugging.    
        print ('First Messier object: ', messierList.objectTable[0].name)

        loopOverMessierObjects = True
        index        = 0
        objectNumber = 1
        while (loopOverMessierObjects):
            x = 0
            if index == len(messierList.objectTable):
                loopOverMessierObjects = False
            else:
                if messierList.objectTable[index].bin() > 0:
                                
                    alt = messierList.objectTable[index].alt.deg

                    if alt > 20.0:
                        messierList.objectTable[index].write()
                        azi = messierList.objectTable[index].azi.deg

                        objectNumber += 1

                        # Grab the input value and attempt to convert it to
                        # an integer
                        
                        x = int(input('1 to observe, 2 to skip, 3 to exit : '))
                        if x == 1:
                        
                            objectRa = messierList.objectTable[index].ra
                            objectDec = messierList.objectTable[index].dec

                            print ('object RA  (hr:min:sec)  : ', objectRa.hr,   ':', objectRa.min,  ':', objectRa.sec)
                            print ('object Dec (deg:min:sec) : ', objectDec.deg, ':', objectDec.min, ':', objectDec.sec)

                            newRa = convertRaDecToCgemUnits.ConvertRa(float(objectRa.hr),
                                                                      float(objectRa.min),
                                                                      float(objectRa.sec)).toCgem()
        
                    
                            newDec = convertRaDecToCgemUnits.ConvertDec(float(objectDec.deg),
                                                                        float(objectDec.min),
                                                                        float(objectDec.sec)).toCgem()

                            newRaHex  = newRa.encode('utf-8')
                            newDecHex = newDec.encode('utf-8')

                            print ('newRaHex  : ', newRaHex)
                            print ('newDecHex : ', newDecHex)
                            
                            print ('Invoking gotoCommandWithHP')
                            cgem.gotoCommandWithHP (newRaHex, newDecHex)

                            telescopeRaDecCgem = cgem.requestHighPrecisionRaDec()
                            print ('telescopeRaDecCgem:', telescopeRaDecCgem)
#                            args = telescopeRaDecCgem.split(',',2)
#                            raFromCgem = convertRa.fromCgem(args[0])
#                            decFromCgem = convertDec.fromCgem(args[1])
#                            print ('RA  : ', raFromCgem)
#                            print ('Dec : ', decFromCgem)
                            print ('---------------------- DONE ------------------')
                            print ()
                        elif x == 3:
                            loopOverMessierObjects = False
                            print ('Setting loopOverMessierObjects to :',
                                   loopOverMessierObjects)
            index += 1

        print ('Finished the list one time, loop again')

        # Attempt to convert this to an integer
        
        y = int(input('1 to loop again, 2 to exit : '))
        if y == 2:
            loopOverAllMessierObjects = False
            print ('setting loopOverMessierObjects to: ',
                   loopOverMessierObjects)
            
        print ('updateObjectTable')
        
        messierList.updateObjectTable()

    # Done - shut down and clean up

    print ('Quitting, closing simulator, and serial interfaces.')
    
    cgem.quitSimulator() # does nothing when operating with telescope
    cgem.closeSerial()
    sp.shutdown()


    
