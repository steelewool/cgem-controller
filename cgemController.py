# For now this is just a basic test. May want to rename it to something like:
# cgemTest if it actually works.

import convertRaDecToCgemUnits
import cgemInterface
import serial
import commands
import time

cgem = cgemInterface.CgemInterface(False)
ra  = convertRaDecToCgemUnits.Ra()
dec = convertRaDecToCgemUnits.Dec()
    
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

#        print 'ra  : ', ra.hr,   ra.min,  ra.sec
#        print 'dec : ', dec.deg, dec.min, dec.sec
#        print

#        print 'r'+ra.toCgem()+','+dec.toCgem()

        print 'Execute the goto command:'

        cgem.gotoCommandWithHP (ra, dec)

cgem.closeSerial()

