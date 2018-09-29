# For now this is just a basic test. May want to rename it to something like:
# cgemTest if it actually works.

import convertRaDecToCgemUnits
import serial
import commands
import time

class CgemInterface:
    def __init__(self, useSerial):
        
        # If useSerial is False, then simulate serial. Will incorporate a
        #    simulator after Zach gets that portion working.
        # If useSerial use hardware serial.
        
        self.useSerial = useSerial
        # Using a hardwired /dev/ttyUSB0 for now.
        
        timeout = 1
        if self.useSerial:
            ser = serial.Serial(port     = '/dev/ttyUSB0',
                                baudrate =           9600,
                                timeout  =   timeoutValue)
            ser.write('Ka')
            data = ser.read(2)
            print 'Read : ', data

            if (data != 'a#'):
                print 'Comm not working and exit'
                commWorking = False
            else:
                commWorking = True
        else:
            commWorking = False
    
    def gotoCommand (self, ra, dec):        
        if self.useSerial:
            ser.write ('r'+ra.toCgem()+','+dec.toCgem())
        else:
            print 'r'+ra.toCgem()+','+dec.toCgem()

#       Confirm command sent to the handcontroller'
        if self.useSerial:
            data = ser.read(1)
        
            gotoInProgress = True
            while (gotoInProgress):
                time.sleep(1)
                ser.write('L')
                data = ser.read(2)
#            print 'Result of L command: ', data
                if (data == '0#'):
                    print 'Goto Finished'
                    gotoInProgress = False
        
    def closeSerial (self):
        ser.close()
        
if __name__ == '__main__':
    print 'Main program for cgemInterface.py'
    
    cgemInterface = CgemInterface(False)
    
    ra = convertRaDecToCgemUnits.Ra()
    dec = convertRaDecToCgemUnits.Dec()
    
    cgemInterface.gotoCommand(ra,dec)
    
