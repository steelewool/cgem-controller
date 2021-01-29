import serial
import spawnSimulator
import convertRaDecToCgemUnits
import cgemInterface
import time

# This program tests the basic serial functions. Originally I had
# motion commands embedded in this code. But those are being removed
# and will live in the test program testMotion.py.

if __name__ == '__main__':
    
    # Request input as to if simulation or using telescope hardware
    
    if input("Enter 1 for simulation 2 for hardware ") == '1':
        simulate = True
    else:
        simulate = False

    sp = spawnSimulator.SpawnSimulator(simulate)

    cgemI = cgemInterface.CgemInterface()

    print ('Comm Working Flag : ', cgemI.commWorking())
    print ('Aligment          : ', cgemI.alignmentComplete())
    print ('GotoInProgress    : ', cgemI.gotoInProgress())

    # cgemI.rtcGetLocation working as of 1/25/21
    print ('RTC location      : ', cgemI.rtcGetLocation())

    # cgemI.getTime working as of 1/25/21
    print ('Time              : ', cgemI.getTime())

#   rtcGetTime not working as of 1/27/21
    print ('Tracking mode     : ', cgemI.getTrackingMode())
    
    convertRa  = convertRaDecToCgemUnits.ConvertRa()
    convertDec = convertRaDecToCgemUnits.ConvertDec()
    
    # The function requestionHighPrecisionRaDec should actually
    # be retruning the RA and Dec and have this additional logic
    # embedded in the function.

    try:
        # requestHighPrecisionRaDec returns the RA and Declination
        # in Cgem units in hex value.
        
        telescopeRaDecCgemI = cgemI.requestHighPrecisionRaDec()

        # The requestHighPrecisionRaDec function returns two values
        # which are extracted below. These two values are used in
        # the gotoCommandWithHP function. Which as of 1/28/21 appears
        # to be working. This has not been verified by verification
        # with the telescope yet.
        
        raHex = telescopeRaDecCgemI[0]
        decHex = telescopeRaDecCgemI[1]
        print ('telescopeRaDecCgem: ', telescopeRaDecCgemI)

        # These two fromCgem functions return the hour,min,sec tuple
        # for the RA and degrees,min,sec tuple for the Declination.
        
        raFromCgem = convertRa.fromCgem(telescopeRaDecCgemI[0])
        decFromCgem = convertDec.fromCgem(telescopeRaDecCgemI[1])

        print ('RA  : ', raFromCgem)
        print ('Dec : ', decFromCgem)
    except:
        print ('requestHighPrecisionRaDec failed')
    
    telescopeRaDecCgemI = cgemI.requestLowPrecisionRaDec()
    print ('telescopeRaDecCgem: ', telescopeRaDecCgemI)
    
    # Done - shut down and clean up

    time.sleep(1)

    print ('Quitting, closing simulator, and serial interfaces.')

    cgemI.quitSimulator() # does nothing when operating with telescope
    cgemI.closeSerial()
    sp.shutdown()

