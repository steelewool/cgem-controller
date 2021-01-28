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

    print ('commWorkingFlag : ', cgemI.commWorking())
    print ('aligment        : ', cgemI.alignmentComplete())
    print ('gotoInProgress  : ', cgemI.gotoInProgress())

    # cgemI.rtcGetLocation working as of 1/25/21
    print ('RTC location    : ', cgemI.rtcGetLocation())

    # cgemI.getTime working as of 1/25/21
    print ('time            : ', cgemI.getTime())

#   rtcGetTime not working as of 1/27/21
#    print ('rtc time        : ', cgemI.rtcGetTime())
    print ('tracking mode   : ', cgemI.getTrackingMode())
    
    convertRa  = convertRaDecToCgemUnits.ConvertRa()
    convertDec = convertRaDecToCgemUnits.ConvertDec()
    
    # The function requestionHighPrecisionRaDec should actually
    # be retruning the RA and Dec and have this additional logic
    # embedded in the function.
    
    telescopeRaDecCgemI = cgemI.requestHighPrecisionRaDec()
    print ('telescopeRaDecCgem: ', telescopeRaDecCgemI)
    
#    raFromCgem = convertRa.fromCgem(args[0])
#    decFromCgem = convertDec.fromCgem(args[1])
#    print ('RA  : ', raFromCgem)
#    print ('Dec : ', decFromCgem)

    telescopeRaDecCgemI = cgemI.requestLowPrecisionRaDec()
    print ('telescopeRaDecCgem: ', telescopeRaDecCgemI)
    
    # Done - shut down and clean up

    time.sleep(1)

    print ('Quitting, closing simulator, and serial interfaces.')

    cgemI.quitSimulator() # does nothing when operating with telescope
    cgemI.closeSerial()
    sp.shutdown()

