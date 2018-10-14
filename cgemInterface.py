# Imports from standard lib
import serial
import commands
import time
import sys
# Provide the interface to the Cgem controller via the serial interface.
import convertRaDecToCgemUnits

# Zach is working on a simulator. My thought is that I should be able
#      to accept as input to the CgemClass a string for setting the port
#      value. Util that is working I'll continue using the useSerial flag
#      to jump around any ser commands.

# 2018-10-12 removed the useSerial argument.

class CgemInterface:
    def __init__(self, port='./pty1'):
        
        # If useSerial is False, then simulate serial. Will incorporate a
        #    simulator after Zach gets that portion working.
        # If useSerial is True, then use hardware serial.
        
        timeoutValue = 1
        
        # For zach I'm changing the serial port form '/dev/ttyUSB0' which
        # was working to ./pty for the test of socat
        
        self.ser = serial.Serial(port     =         port,
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
    
    # 'length' should include the final delimiter in the expected response
    def readSerial(self, length):
        output = ""
        nullCount = 0
        while len(output) < length and nullCount < 10:
            output = output.strip("#")
            newContent = str(self.ser.read_until('#'))
            output += newContent
            if newContent == "":
                nullCount += 1
        # Log errors to console for now
        if nullCount == 10:
            print "ERROR: Unable to complete read operation; no response from serial device"
        return output
    
    def gotoCommandWithHP (self, ra, dec):
        raToCgem  = ra.toCgem()
        decToCgem = dec.toCgem()
        self.ser.write ('r'+raToCgem+','+decToCgem)
        print 'gotoCommand: r'+raToCgem+','+decToCgem

        data = self.readSerial(1)
        print 'Read after gotoCommand:',data
            
        gotoInProgress = True
        while (gotoInProgress):
            time.sleep(1)
            self.ser.write('L')
                
            data = self.readSerial(2)
            print 'Result of L command:', data
            if (data == '0#'):
                print 'Goto Finished'
                gotoInProgress = False

    def gotoCommandWithLP (self, ra, dec):
        print 'Not implemented'
                            
    def requestHighPrecisionRaDec (self):
        self.ser.write ('e')
        result = self.readSerial(18);
        return result
    
    def requestLowPrecisionRaDec (self):
        ser.write ('E')
        result = self.readSerial(10)
        return result       
        
    def closeSerial(self):
        print 'closing serial interface'
        self.ser.close()

if __name__ == '__main__':
    
    cgemInterface = CgemInterface()
    
    ra  = convertRaDecToCgemUnits.Ra()
    dec = convertRaDecToCgemUnits.Dec()
    
    ra.hr = 15
    ra.min = 14
    ra.sec = 13
    
    dec.deg = 0
    dec.min = 20
    dec.min = 10
    
    cgemInterface.gotoCommandWithHP (ra, dec)
    print 'result of move:', cgemInterface.requestHighPrecisionRaDec()

