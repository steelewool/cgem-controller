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

    cgem = cgemInterface.CgemInterface()

    print ('commWorkingFlag : ', cgem.commWorking())
    print ('aligment        : ', cgem.alignmentComplete())
    print ('gotoInProgress  : ', cgem.gotoInProgress())
    print ('location        : ', cgem.getLocation())
    print ('time            : ', cgem.getTime())
    print ('tracking mode   : ', cgem.getTrackingMode())
    
    convertRa  = convertRaDecToCgemUnits.ConvertRa()
    convertDec = convertRaDecToCgemUnits.ConvertDec()
    
    # The function requestionHighPrecisionRaDec should actually
    # be retruning the RA and Dec and have this additional logic
    # embedded in the function.
    
    telescopeRaDecCgem = cgem.requestHighPrecisionRaDec()
    print ('telescopeRaDecCgem: ', telescopeRaDecCgem)
    #args = telescopeRaDecCgem.split(',',2)
    #print ('args 0 & 1: ', args[0], ' ', args[1])
    
#    raFromCgem = convertRa.fromCgem(args[0])
#    decFromCgem = convertDec.fromCgem(args[1])
#    print ('RA  : ', raFromCgem)
#    print ('Dec : ', decFromCgem)

    telescopeRaDecCgem = cgem.requestLowPrecisionRaDec()
    print ('telescopeRaDecCgem: ', telescopeRaDecCgem)
    #args = telescopeRaDecCgem.split(',',2)
    #print ('args 0 & 1: ', args[0], ' ', args[1])

    # Done - shut down and clean up

    time.sleep(1)

    print ('Quitting, closing simulator, and serial interfaces.')

    cgem.quitSimulator() # does nothing when operating with telescope
    cgem.closeSerial()
    sp.shutdown()

