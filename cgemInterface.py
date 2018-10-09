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

class CgemInterface:
    def __init__(self, useSerial, port='./pty1'):
        
        # If useSerial is False, then simulate serial. Will incorporate a
        #    simulator after Zach gets that portion working.
        # If useSerial is True, then use hardware serial.
        
        self.useSerial = useSerial
        # Using a hardwired /dev/ttyUSB0 for now.
        
        timeoutValue = 1
        
        # For zach I'm changing the serial port form '/dev/ttyUSB0' which
        # was working to ./pty for the test of socat
        
        if self.useSerial:
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
        else:
            commWorking = False
    
    # 'length' should include the final delimiter in the expected response
    def readSerial(self, length):
        output = ""
        nullCount = 0
        readLimit = 60
        readCount = 0
        while len(output) < length and nullCount < 10 and readCount < readLimit:
            output = output.strip("#")
            newContent = str(self.ser.read_until('#'))
            output += newContent
            print "Partial read:", output
            if newContent == "":
                print "No data from serial device"
                nullCount += 1
            readCount += 1
        if readCount == readLimit:
            print "Retry limit exceeded, unable to reach target character length"
        # Log errors to console for now
        if nullCount == 10:
            print "ERROR: Unable to complete read operation; no response from serial device"
        return output
    
    def gotoCommandWithHP (self, ra, dec):
        if self.useSerial:
            self.ser.write ('r'+ra.toCgem()+','+dec.toCgem())
            print 'gotoCommand: r'+ra.toCgem()+','+dec.toCgem()
        else:
            print 'r'+ra.toCgem()+','+dec.toCgem()
        
        if self.useSerial:
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
        if self.useSerial:
            self.ser.write ('e')
            result = self.readSerial(18);
        else:
            result = 'xxxxx#'
        return result
    
    def requestLowPrecisionRaDec (self):
        if self.userSerial:
            ser.write ('E')
            result = self.readSerial(10)
        else:
            result = 'xxxxx#'
        return result       
        
    def closeSerial(self):
        if self.useSerial:
            print 'closing serial interface'
            self.ser.close()

if __name__ == '__main__':
    
    port = './pty1'
    if len(sys.argv) > 1:
        port = sys.argv[1]
    
    cgemInterface = CgemInterface(True, port)
    
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

