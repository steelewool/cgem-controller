# This program is setup to observe Messier objetcs.

# I'm not using the alt/azi to determine if the object is above the horizon
# and I should be.

import spawnSimulator
import convertRaDecToCgemUnits
import cgemInterface
import messierObjectList

if __name__ == '__main__':

    # Request input as to if simulation or using telescope hardware
    
    if input("Enter 1 for simulation 2 for hardware ") == '1':
        simulate = True
        print ('Simulate set to true')
    else:
        simulate = False
        print ('Simulate set to false')

    # This will either spawn a shell program for setting up the
    # ports for a simulator or for debugging and talking to the
    # telescope.

    print ('spawnSimulator')
    
    sp = spawnSimulator.SpawnSimulator(simulate)

    print ('Done with spawnSimulator.SpawnSimulator, with argument: ', simulate)
    
    # The initializer for cgemInterface will open the serial port.
    # The default is ./pty1 which works with either the simulator
    # using nullmodem.sh or when using socat. If talking directly
    # to real hardware will want to set port = '/dev/ttyUSB0'
    # or something simular.

    print ('Invoke cgemInterface.CgemInterface()')
    
    cgem       = cgemInterface.CgemInterface()

    print ('Done with cgemInterface.CgemInterface()')
    
    convertRa  = convertRaDecToCgemUnits.Ra()
    convertDec = convertRaDecToCgemUnits.Dec()
    
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

                        print ('  Name : ', messierList.objectTable[index].name)
                        print ('   alt : ', alt)
                        print ('   azi : ', azi)
                        print

                        # Grab the input value and attempt to convert it to an integer
                        
                        x = int(input('1 to observe, 2 to skip, 3 to exit '))
                        print ('x: ', x)
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

                            print ('Invoking requestHighPrecision')
                            telescopeRaDecCgem = cgem.requestHighPrecisionRaDec()
                            args = telescopeRaDecCgem.split(',',2)
                            raFromCgem = convertRa.fromCgem(args[0])
                            decFromCgem = convertDec.fromCgem(args[1])
                            print ('RA  : ', raFromCgem)
                            print ('Dec : ', decFromCgem)
                            print
                        elif x == 3:
                            loopOverAllMessierObjects = False
                            print ('Setting loopOverAllMessierObjects to :',
                                   loopOverAllMessierObjects)
            index += 1

        print
        print ('Finished the list one time, loop again')
        print

        # Attempt to convert this to an integer
        
        y = int(input('1 to loop again, 2 to exit'))
        if y == 2:
            loopOverAllMessierObjects = False
            print ('setting loopOverAllMessierObjects to: ',
                   loopOverAllMessierObjects)
            
        print ('updateObjectTable')
        
        messierList.updateObjectTable()

    # Done - shut down and clean up

    print ('Quitting, closing simulator, and serial interfaces.')
    
    cgem.quitSimulator() # does nothing when operating with telescope
    cgem.closeSerial()
    sp.shutdown()


    
