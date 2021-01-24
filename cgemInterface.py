# Imports from standard lib

import keyboard
import serial
import command
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
    
    # The initializer defaults to .pty1 which is used in the
    # simulation (nullmodel.sh) and when socat is used for debugging
    
    def __init__(self, port='./pty1'):
        
        timeoutValue = 1
        
        # For zach I'm changing the serial port form
        # '/dev/ttyUSB0' which
        # was working to ./pty for the test of socat
        
        self.ser = serial.Serial(port     =         port,
                                 baudrate =         9600,
                                 timeout  = timeoutValue)

        print ('try self.ser.write with b Ka')
        
        self.ser.write(b'Ka')
        data = self.ser.read(2)
        print ('Read : ', data)
            
        if (data != 'a#'):
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
            print ('ERROR: Unable to complete read operation; no response from serial device')
        return output
    
    def gotoCommandWithHP (self, ra, dec):
        
        # Since I'm using the results of toGem for debugging
        # I only to the conversion once and then use the variables
        # raToCgem and decToCgem in the serial write and the print
        
        raToCgem  = ra.toCgem()
        decToCgem = dec.toCgem()

        print ('gotoCommand: r'+raToCgem+','+decToCgem)

        # Having errors getting this to write to the telescope,
        # will try in two steps.
        # self.ser.write ('r'+raToCgem+','+decToCgem)

        writeString = 'r'+raToCgem+','+decToCgem
        self.ser.write (b'r69EE8D00,318CCD00')

        data = self.readSerial(1)
        print ('Read after gotoCommand:',data)
            
        gotoInProgress = True

        #Getting an error that I must be root to use keyboard.is_pressed.
        
#        while (gotoInProgress):

#            if keyboard.is_pressed('space'):
#                print ('Detected a key got pressed')
#                self.cancelGoto()
#                # some key got pressed
#                # send command to stop gotoCommand
#                gotoInProgress = False
#            time.sleep(1)

#            print ('self.ser.write L')
            
#            self.ser.write(b'L')
                
#            data = self.readSerial(2)
#            print 'Result of L command:', data
#            if (data == '0#'):
#                print ('Goto Finished')
#                gotoInProgress = False

    def gotoCommandWithLP (self, ra, dec):
        print ('Not implemented')

    def cancelGoto (self):
        print ('self.ser.write M')
        self.ser.write (b'M')
        result = self.readSerial(1)
        return result
    
    def requestHighPrecisionRaDec (self):
        print ('self.ser.write e')
        self.ser.write (b'e')
        result = self.readSerial(18)
        print ('In requestHighPrecisionRaDec, result: ', result)
        findHashTag = result.find('#')
        print ('in requestHighPrecisionRaDec, findHashTag:', findHashTag)
        if findHashTag < 0:
            result = self.readSerial(18)
            print ('second read, result: ', result)
            findHashTag = result.find('#')
        if findHashTag > 0:                        
            result = result[0:findHashTag]
        return result
    
    def requestLowPrecisionRaDec (self):
        print ('self.ser.write E')
        ser.write (b'E')
        result = self.readSerial(10)
        return result       

    def quitSimulator (self):
        print ('self.ser.write q')
        self.ser.write(b'q')
        
    def closeSerial(self):
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
    print ('result of move:', cgemInterface.requestHighPrecisionRaDec())

    cgemInterface.quitSimulator()
    
