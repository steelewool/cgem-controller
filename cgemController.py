# For now this is just a basic test. May want to rename it to something like:
# cgemTest if it actually works.

import convertRaDecToCgemUnits
import serial

import commands

ra  = convertRaDecToCgemUnits.Ra()
dec = convertRaDecToCgemUnits.Dec()

# Setting a 1 second timeout

timeoutValue = 1

# Get and list the possible serial ports

print commands.getstatusoutput ('ls /dev/ttyUSB*')

# serialPort = input ("Enter serial port, something like 'ttyUSB0' for example ")

# Using a hardwired /dev/ttyUSB0 for now.

ser = serial.Serial(port     = '/dev/ttyUSB0',
                    baudrate =           9600,
                    timeout  =   timeoutValue)

print 'ser name : ', ser.name

# Do a read of the serial port with the idea to clear out
# any characters that may be sitting there.

print 'Do a read of the serial with the timeout of: ', timeoutValue

data = ser.read(50)
print 'data : ', data
loopControl = True

print 'Enter a negative number for the RA hours wnd the loop will exit.'

while loopControl:
    ra.hr   = input ('raHr   : ')

    if ra.hr <= -1:
        print 'User specified time to quit'
        loopControl = False
    else:
        ra.min  = input ('raMin  : ')
        ra.sec  = input ('raSec  : ')
    
        dec.deg = input ('decDeg : ')
        dec.min = input ('decMin : ')
        dec.sec = input ('decSec : ')

        print 'ra  : ', ra.hr,   ra.min,  ra.sec
        print 'dec : ', dec.deg, dec.min, dec.sec
        print

        print 'r'+ra.toCgem()+','+dec.toCgem()

        ser.write ('r'+ra.toCgem()+','+dec.toCgem())
        
        # Hand controller should respond with a # character

        # print 'Changed the timeout value to: ', ser.timeout
        foundHashTag = True

        while (foundHashTag):
            data = ser.read(1)
            print 'data : ', data
            if (data == '#'):
                print 'found the hash tag'
                foundHashTag = False
        print

        ser.write(b'e')            # write a string
        foundHashTag = True

        output = ''

        while (foundHashTag):
            data = ser.read(1)
            output = output + data
            if (data == '#'):
                foundHashTag = False
        print 'output: ', output

ser.close()
