import serial
import spawnSimulator
import convertRaDecToCgemUnits
import cgemInterface
import time

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
        telescopeRaDecCgemI = cgemI.requestHighPrecisionRaDec()
        raHex = telescopeRaDecCgemI[0]
        decHex = telescopeRaDecCgemI[1]
        print ('telescopeRaDecCgem: ', telescopeRaDecCgemI)
    
        raFromCgem = convertRa.fromCgem(telescopeRaDecCgemI[0])
        decFromCgem = convertDec.fromCgem(telescopeRaDecCgemI[1])

        print ('RA  : ', raFromCgem)
        print ('Dec : ', decFromCgem)
    except:
        print ('requestHighPrecisionRaDec failed')

    try:
        cgemI.gotoCommandWithHP (raHex, decHex)
    except:
        print ('gotoCommandWithHP failed')
    
    telescopeRaDecCgemI = cgemI.requestLowPrecisionRaDec()
    print ('telescopeRaDecCgem: ', telescopeRaDecCgemI)
    
    # Done - shut down and clean up

    time.sleep(1)

    print ('Quitting, closing simulator, and serial interfaces.')

    cgemI.quitSimulator() # does nothing when operating with telescope
    cgemI.closeSerial()
    sp.shutdown()

