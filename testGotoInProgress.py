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

    print ('Echo command      : ', cgemI.echoCommand(b'a'))
    print ('Comm Working Flag : ', cgemI.commWorking())
    print ('Aligment          : ', cgemI.alignmentComplete())
    print ('GotoInProgress    : ', cgemI.gotoInProgress())
    print ('RTC location      : ', cgemI.rtcGetLocation())
    print ('Time              : ', cgemI.getTime())
    print ('Tracking mode     : ', cgemI.getTrackingMode())

    time.sleep(3)

    print ('Quitting, closing simulator, and serial interfaces.')

    cgemI.quitSimulator() # does nothing when operating with telescope
    cgemI.closeSerial()
    sp.shutdown()

