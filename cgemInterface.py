# Imports from standard lib

import keyboard
import serial
import command
import time
import sys

# Provide the interface to the Cgem controller via the serial interface.
# All of the commands to read & write data to and from the CGEM telesope
# are implement here.

import convertRaDecToCgemUnits


# Zach is working on a simulator. My thought is that I should be able
#      to accept as input to the CgemClass a string for setting the port
#      value. Util that is working I'll continue using the useSerial flag
#      to jump around any ser commands.

# 2018-10-12 removed the useSerial argument.

convertRa  = convertRaDecToCgemUnits.ConvertRa()
convertDec = convertRaDecToCgemUnits.ConvertDec()

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

    def serialRead (self, waitTime, bytes):
        time.sleep(waitTime)
        return self.ser.read(bytes)
    
    def echoCommand (self, testCharacter):
        print ('In echoCommand')
        self.ser.write(b'Ka')

        # The mechanism of just using the raw ser.read command to read
        # data from the telescope seems a lot less complicated that using
        # a general read command (like readSerial). Unless there is some
        # error recover logic I can think of just stripping off the last
        # hashtag character (#) seems easy enough.
        
        response = self.serialRead(waitTime=3,bytes=2)
        print ('In echoCommand, response: ', response)
        return response

    def commWorking(self):
 #       print ('in commWorking')
        response = self.echoCommand('a')
        if len(response) != 2:
            print ('incorrect length response')
            return 'Comm Failure ' + str(len(response))

        if (response != b'a#'):
            commWorkingFlag = False
        else:
            commWorkingFlag = True
        return commWorkingFlag
    
    def alignmentComplete (self):
        self.ser.write(b'J')
        response = self.serialRead(waitTime=3,bytes=2)
        if len(response) != 2:
            print ('Incorrect response length')
            return 'Comm Failure ' + str(len(response))
        if response[0] == 0:
            alignment = False
        else:
            alignment = True
        return alignment

    def gotoInProgress (self):
        self.ser.write(b'L')
        response = self.serialRead(waitTime=2,bytes=2)
        if len(response) != 2:
            print ('incorrect response length in gotoInProgress')
            return 'Comm Failure ' + str(len(response))
        print ('gotoInProgress response[0]: ', response[0])

        # A '0' indicates that the motion is in progress.
        # A '1' indicates that the motion has completed.
        # My attempt at using '0' or 48 are both not working.

        if response[0] == 48:
            gotoInProgressFlag = True
        else:
            gotoInProgressFlag = False
        return gotoInProgressFlag

    def rtcGetLocation (self):
        self.ser.write(b'w')
        response = self.serialRead(waitTime=4,bytes=9)
        if len(response) != 9:
            print ('incorrect length response')
            return 'Comm Failure ' + str(len(response))
        latitude = float(response[0])+float(response[1])/60.0+float(response[2])/3600.0
        longitude = float(response[4])+float(response[5])/60.0+float(response[6])/3600.0
        if response[3] == '1':
            latitude = latitude*-1.0
            longitude = float(response[4])+float(response[5])/60.0+float(response[6])/3600.0
        if response[7] == '1':
            longitude = longitude*-1.0
        return [latitude,  response[0], response[1], response[2], response[3],
                longitude, response[4], response[5], response[6], response[7]]
    
    def getTime (self):
        self.ser.write(b'h')
        response = self.serialRead(waitTime=3,bytes=9)
        if len(response) != 9:
            print ('Incorrect response length')
            return 'Comm Failure ' + str(len(response))

        hour  = int(response[0])
        min   = int(response[1])
        sec   = int(response[2])
        month = int(response[3])
        day   = int(response[4])
        year  = int(response[5])+2000
        gmt   = 256-int(response[6])
        if response[7] == '0':
            standardTime = True
        else:
            standardTime = False
        return [hour,min,sec,month,day,year,gmt,standardTime]

    def rtcSetYear (self, x, y):
        print ('In rtcSetYear. x,y: ', x, ',', y)
        baseCommand = 'P'+chr(3)+chr(178)+chr(132)+chr(int(x)*256)+chr(int(year))+chr(0)+chr(0)
        command = baseCommand.encode('utf-8')
        self.ser.write(command)
        response = self.serialRead(waitTime=3,bytes=1)
        print ('rtcSetTime: ', response)

    def rtcSetDate (self, month, year):
        print ('in rtcSetDate');
        baseCommand = 'P'+chr(3)+chr(178)+chr(131)+chr(int(month))+chr(int(year))+chr(0)+chr(0)
        command = baseCommand.encode('utf-8')
        self.ser.write(command)
        response = self.serialRead(waitTime=3,bytes=1)
        if len(response) != 1:
            print ('Incorrect response length')
            return 'Comm Failure ' + str(len(response))
        print ('rtcSetTime: ', response)
        return [response[0]]

    def rtcSetTime (self, hour, min, sec):
        print ('In rtcSetTime')
        baseCommand = 'P'+chr(4)+chr(178)+chr(179)+chr(int(hour))+chr(int(min))+chr(int(sec))+chr(0)
        command = baseCommand.encode('utf-8')
        self.ser.write(command)
        response = self.serialRead(waitTime=3,bytes=1)
        print ('rtcSetTime len(response): ', len(response))
        print ('rtcSetTime: ', response)

    def getTrackingMode (self):
        self.ser.write (b't')
        response = self.serialRead(waitTime=3,bytes=2)
        if len(response) != 2:
            print ('Incorrect response length')
            return 'Comm Failure ' + str(len(response))

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
        print ('In gotoCommandWithHP')
        
        # I only to the conversion once and then use the variables
        # raToCgem and decToCgem in the serial write and the print

        # Having errors getting this to write to the telescope,
        # will try in two steps.
        # self.ser.write ('r'+raToCgem+','+decToCgem)

        writeString = b'r'+ra+b','+dec
        print ('writeString : ', writeString)

        self.ser.write (writeString)

        data = self.serialRead(3,1)
        print ('Read after gotoCommand:',data)

        if data == b'#':
            print ('Valid response, a #')
        else:
            print ('Invalid response not a #')
            
        gotoInProgressFlag = True

        #Getting an error that I must be root to use keyboard.is_pressed.
        
#        while (gotoInProgressFlag):

#            if keyboard.is_pressed('space'):
#                print ('Detected a key got pressed')
#                self.cancelGoto()
#                # some key got pressed
#                # send command to stop gotoCommand
#                gotoInProgress = False

        motionFlag = self.gotoInProgress()
        print ('motionFlag: ', motionFlag)

        motionFlag = self.gotoInProgress()
        print ('motionFlag: ', motionFlag)

        motionFlag = self.gotoInProgress()
        print ('motionFlag: ', motionFlag)
        
        motionFlag = self.gotoInProgress()
        print ('motionFlag: ', motionFlag)
        
        motionFlag = self.gotoInProgress()
        print ('motionFlag: ', motionFlag)

        motionFlag = self.gotoInProgress()
        print ('motionFlag: ', motionFlag)

        motionFlag = self.gotoInProgress()
        print ('motionFlag: ', motionFlag)
        
        motionFlag = self.gotoInProgress()
        print ('motionFlag: ', motionFlag)
        
        gotoInProgressFlag = True


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
        print ('In requestHighPrecisionRaDec')
        self.ser.write (b'e')
        response = self.serialRead(waitTime=3,bytes=18)
        if len(response) != 18:
            print ('Incorrect response length')
            return 'Comm Failure ' + str(len(response))

        commaLocation = response.find(b',')
        hashTagLocation = response.find(b'#')
        raHex = response[0:commaLocation]
        decHex = response[commaLocation+1:hashTagLocation]
        print ('raHex, decHex ', raHex, ' ', decHex)

        return [raHex, decHex]
    
    def requestLowPrecisionRaDec (self):
        print ('In requestLowPrecisionRaDec')
        self.ser.write (b'E')
        response = self.serialRead(3,10)
        if len(response) != 10:
            print ('Incorrect response length')
            return 'Comm Failure ' + str(len(response))

        commaLocation = response.find(b',')
        hashTagLocation = response.find(b'#')
        raHex = response[0:commaLocation]
        decHex = response[commaLocation+1:hashTagLocation]
        print ('raHex, decHex ', raHex, ' ', decHex)

        return [raHex, decHex]

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
    
