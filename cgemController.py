# For now this is just a basic test. May want to rename it to something like:
# cgemTest if it actually works.

import convertRaDecToCgemUnits
import serial

ra  = convertRaDecToCgemUnits.Ra()
dec = convertRaDecToCgemUnits.Dec()

# Setting a 5 second timeout - which seems too long
# But good to start experimenting with.

timeoutValue = 1

ser = serial.Serial('/dev/ttyUSB0', timeout=timeoutValue)
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

        print 'ra  : ', ra.hr, ra.min, ra.sec
        print 'dec : ', dec.deg, dec.min, dec.sec
        print

        print 'r'+ra.toCgem()+','+dec.toCgem()
        
        ser.write ('r'+ra.toCgem()+','+dec.toCgem())

        ser.timeout = 60

        print 'Changed the timeout value to: ', ser.timeout
        tried = 120
        foundHashTag = False
        while ((tries > 0) or foundHashTag):
            data = ser.read(1)
            print 'data : ', data
            if (data == '#'):
                foundHashTag = True
        print

        # Hand controller should respond with a # character


