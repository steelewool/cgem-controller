# Provide the interface to the Cgem controller via the serial interface.

import convertRaDecToCgemUnits
import serial
import commands
import time

# Zach is working on a simulator. My thought is that I should be able
#      to accept as input to the CgemClass a string for setting the port
#      value. Util that is working I'll continue using the useSerial flag
#      to jump around any ser commands.

class CgemInterface:
    def __init__(self, useSerial, port='./pty'):
        
        # If useSerial is False, then simulate serial. Will incorporate a
        #    simulator after Zach gets that portion working.
        # If useSerial is True, then use hardware serial.
        
        self.useSerial = useSerial
        # Using a hardwired /dev/ttyUSB0 for now.
        
        timeoutValue = 1
        
        # For zach I'm changing the serial port form '/dev/ttyUSB0' which
        # was working to ./pty for the test of socat
        
        if self.useSerial:
            self.ser = serial.Serial(port     =    self.port,
                                     baudrate =         9600,
                                     timeout  = timeoutValue)
            self.ser.write('Ka')
            data = self.ser.read(2)
            print 'Read : ', data

            if (data != 'a#'):
                print 'Comm not working and exit'
                commWorking = False
            else:
                commWorking = True
        else:
            commWorking = False
    
    def gotoCommandWithHP (self, ra, dec):
        if self.useSerial:
            self.ser.write ('r'+ra.toCgem()+','+dec.toCgem())
            print 'gotoCommand : r'+ra.toCgem()+','+dec.toCgem()
        else:
            print 'r'+ra.toCgem()+','+dec.toCgem()

        if self.useSerial:
            data = self.ser.read(1)
        
            gotoInProgress = True
            while (gotoInProgress):
                time.sleep(1)
                self.ser.write('L')
                data = self.ser.read(2)
                if (data == '0#'):
                    print 'Goto Finished'
                    gotoInProgress = False
        
    def requestHighPrecisionRaDec (self):
        if self.useSerial:
            self.ser.write ('e')
            result = self.ser.read(20)
        else:
            result = 'xxxxx#'
        return result
    
    def closeSerial(self):
        if self.useSerial:
            print 'closing serial interface'
            self.ser.close()

if __name__ == '__main__':

    cgemInterface = CgemInterface(False)
    
    ra  = convertRaDecToCgemUnits.Ra()
    dec = convertRaDecToCgemUnits.Dec()
    
    ra.hr = 15
    ra.min = 14
    ra.sec = 13
    
    dec.deg = 0
    dec.min = 20
    dec.min = 10
    
    cgemInterface.gotoCommand(ra, dec)
    print 'resultant ra/dec: ', CgemInterface.requestHighPrecisionRaDec()
    