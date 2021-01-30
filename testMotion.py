# This program was created by copying testSerial.py.
# I used the vesion from commit
# 705263d1b9618d6fe2daa54f083975277939f76e

import serial
import spawnSimulator
import convertRaDecToCgemUnits
import cgemInterface
import time

if __name__ == '__main__':

    # Hardware this to work only with actual hardware
    
    simulate = False

    sp = spawnSimulator.SpawnSimulator(simulate)

    cgemI = cgemInterface.CgemInterface()

    print ('Aligment          : ', cgemI.alignmentComplete())

    # Not sure with these definitions are necessary,
    # but they might shorthand the code.
    
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

        print ('RA (hr,  min, sec) : ', raFromCgem)
        print ('Dec(deg, min, sec) : ', decFromCgem)
    except:
        print ('requestHighPrecisionRaDec failed')

    try:
        print ('Calling gotoCommandWithHP')
        print ('     raHex  : ', raHex)
        print ('     decHex : ', decHex)
        cgemI.gotoCommandWithHP (raHex, decHex)
    except:
        print ('gotoCommandWithHP failed')
    
    # Try and drive the telescope:

    newRa = convertRaDecToCgemUnits.ConvertRa(float( 3),
                                              float(21),
                                              float(52)).toCgem()
        
    newRaHex = newRa.encode('utf-8')
    
    newDec = convertRaDecToCgemUnits.ConvertDec(float(89),
                                                float(57),
                                                float(37)).toCgem()

    newDecHex = newDec.encode('utf-8')
    
    print ('newRa     : ', newRa)
    print ('newDec    : ', newDec)
    print ('newRaHex  : ', newRaHex)
    print ('newDecHex : ', newDecHex)
    
    cgemI.gotoCommandWithHP (newRaHex, newDecHex)
    
    # Done - shut down and clean up

    time.sleep(1)

    print ('Quitting, closing simulator, and serial interfaces.')

    cgemI.quitSimulator() # does nothing when operating with telescope
    cgemI.closeSerial()
    sp.shutdown()
