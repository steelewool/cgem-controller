# For now this is just a basic test. May want to rename it to something like:
# cgemTest if it actually works.

import convertRaDecToCgemUnits
import serial
import commands
import time

ra  = convertRaDecToCgemUnits.Ra()
dec = convertRaDecToCgemUnits.Dec()

timeoutValue = 1
# Get and list the possible serial ports
#print commands.getstatusoutput ('ls /dev/ttyUSB*')

# serialPort = input ("Enter serial port, something like 'ttyUSB0' for example ")
# Using a hardwired /dev/ttyUSB0 for now.
ser = serial.Serial(port     = '/dev/ttyUSB0',
                    baudrate =           9600,
                    timeout  =   timeoutValue)
print 'ser name : ', ser.name
#data = ser.read(50)
#print 'data : ', data

# Do a read of the serial port with the idea to clear out
# any characters that may be sitting there.

print 'Test communication to the device by sending a Ka'
print 'Hand controllers should return with a#'

ser.write('Ka')
data = ser.read(2)
print 'Read : ', data

if (data != 'a#'):
    print 'Comm not working and exit'
    exit()
    
print 'Enter a negative number for the RA hours wnd the loop will exit.'

loopControl = True
while loopControl:
    ra.hr   = input ('raHr   : ')
    
# Touch base, with Zach, see if using an exit() here would by python like?

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

        print 'Execute the goto command:'
        
        ser.write ('r'+ra.toCgem()+','+dec.toCgem())
        
#       Confirm command sent to the handcontroller'
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

        print 'Goto complete, now request where it moved to.'
        
        ser.write('e')            # write a string
        print 'output: ', ser.read(20)

ser.close()
