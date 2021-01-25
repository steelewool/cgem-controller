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

        
        # Continuing with the software does not make a lot of sense if the comm
        # is not working. But, currently the software just charges ahead.
    
    # testcharacter is not being used until I get the details of
    # sending and receiving data worked out. For now, I'll just
    # send a hard wired 'a' character

    def serialRead (self, timeout, bytes):
        time.sleep(timeout)
        return self.ser.read(bytes)
    
    def echoCommand (self, testCharacter):

        self.ser.write(b'Ka')

        # The mechanism of just using the raw ser.read command to read
        # data from the telescope seems a lot less complicated that using
        # a general read command (like readSerial). Unless there is some
        # error recover logic I can think of just stripping off the last
        # hashtag character (#) seems easy enough.
        
        response = self.serialRead(3,2)
        print ('In echoCommand, response: ', response)
        return response

    def commWorking(self):
        response = self.echoCommand('a')
        if (response != b'a#'):
            commWorkingFlag = False
        else:
            commWorkingFlag = True
        return commWorkingFlag
    
    def alignmentComplete (self):
        self.ser.write(b'J')
        response = self.serialRead(3,2)
        print ('In alignmentComplete, response    : ', response)
        print ('In alignmentComplete, response[0] : ', response[0])
        if response[0] == '0':
            alignment = False
        else:
            alignment = True
        return alignment

    def gotoInProgress (self):
        self.ser.write(b'L')
        response = self.serialRead(3,2)
        if response[0] == '0':
            gotoInProgessFlag = False
        else:
            gotoInProgressFlag = True
        return gotoInProgressFlag

    def getLocation (self):
        self.ser.write(b'w')
        response = self.serialRead(3,9)
        print ('get location, bytes 1-8: ',
               response[0], ' ',
               response[1], ' ',
               response[2], ' ',
               response[3], ' ',
               response[4], ' ',
               response[5], ' ',
               response[6], ' ',
               response[7])
        latitude = float(response[0]) + float(response[1])/60.0 + float(response[2])/3600.0
        if response[3] == '1':
            latitude = latitude*-1.0
        longitude = float(response[4]) + float(response[5])/60.0 + float(response[6])/3600.0
        if response[7] == '1':
            longitude = longitude*-1.0
        return [latitude,  response[0], response[1], response[2], response[3],
                longitude, response[4], response[5], response[6], response[7]]
    
    def getTime (self):
        self.ser.write(b'h')
        response = self.serialRead(3,9)
        print ('get time response: ', response)
        print ('get time, bytes 1-8: ',
               response[0], ' ',
               response[1], ' ',
               response[2], ' ',
               response[3], ' ',
               response[4], ' ',
               response[5], ' ',
               response[6], ' ',
               response[7])
        hour  = int(response[0])
        min   = int(response[1])
        sec   = int(response[2])
        month = int(response[3])
        day   = int(response[4])
        year  = int(response[5])+2000
        gmt   = int(response[6])
        if response[7] == '0':
            standardTime = True
        else:
            standardTime = False
        return [hour,min,sec,month,day,year,gmt,standardTime]

    def getTrackingMode (self):
        self.ser.write (b't')
        response = self.serialRead(3,2)
        print ('getTrackingMode, response: ', response)
        trackingMode = 'Undefined'
        if response[0] == 0:
            trackingMode = 'Off'
        elif response[0] == 1:
            trackingMode = 'Alt/Azi'
        elif response[0] == 2:
            trackingMode = 'EQ North'
        elif response[0] == 3:
            trackingMode = 'EQ South'
        return trackingMode

    # Go to a RA/Dec position using the high precision mode.
    
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

        data = self.serialRead(3,1)
        print ('Read after gotoCommand:',data)
            
        #gotoInProgress = True

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
                
#            data = self.serialRead(3,2)
#            print 'Result of L command:', data
#            if (data == '0#'):
#                print ('Goto Finished')
#                gotoInProgress = False

    def gotoCommandWithLP (self, ra, dec):
        print ('Not implemented')

    def cancelGoto (self):
        print ('self.ser.write M')
        self.ser.write (b'M')
        result = self.serialRead(3,1)
        return result

    # The function requestionHighPrecisionRaDec should actually
    # be retruning the RA and Dec and have this additional logic
    # embedded in the function.
        
    def requestHighPrecisionRaDec (self):
        self.ser.write (b'e')
        response = self.serialRead(3,18)
        print ('requestHighPrecisionRaDec, bytes 1-17: ',
               response [0], ' ',
               response [1], ' ',
               response [2], ' ',
               response [3], ' ',
               response [4], ' ',
               response [5], ' ',
               response [6], ' ',
               response [7], ' ',
               response [8], ' ',
               response [9], ' ',
               response[10], ' ',
               response[11], ' ',
               response[12], ' ',
               response[13], ' ',
               response[14], ' ',
               response[15], ' ',
               response[16])
               
        #findHashTag = response.find('#')
        #print ('in requestHighPrecisionRaDec, findHashTag:', findHashTag)
        #if findHashTag > 0:                        
        #    response = response[0:findHashTag]
        return response
    
    def requestLowPrecisionRaDec (self):
        self.ser.write (b'E')
        response = self.serialRead(3,10)
        print ('requestLowPrecisionRaDec, bytes 1-9: ',
               response[0], ' ',
               response[1], ' ',
               response[2], ' ',
               response[3], ' ',
               response[4], ' ',
               response[5], ' ',
               response[6], ' ',
               response[7], ' ',
               response[8])
        return response       

    def quitSimulator (self):
        self.ser.write(b'q')
        
    def closeSerial(self):
        self.ser.close()

if __name__ == '__main__':
    
    cgemInterface = CgemInterface()

    
    #ra  = convertRaDecToCgemUnits.Ra()
    #dec = convertRaDecToCgemUnits.Dec()
    
    #ra.hr = 15
    #ra.min = 14
    #ra.sec = 13
    
    #dec.deg = 0
    #dec.min = 20
    #dec.min = 10
    
    #cgemInterface.gotoCommandWithHP (ra, dec)
    #print ('response of move:', cgemInterface.requestHighPrecisionRaDec())

    cgemInterface.quitSimulator()
    
