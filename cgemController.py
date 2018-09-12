import convertRaDecToCgemUnits
import serial

ra  = convertRaDecToCgemUnits.Ra()
dec = convertRaDecToCgemUnits.Dec()

ser = serial.Serial('/dev/ttyUSB0', timeout=1)
print 'ser name : ', ser.name

loopControl = True

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

        print 'r'+ra.toCgem()+','+dec.toCgem()+'#'
        ser.write ('r'+ra.toCgem()+','+dec.toCgem()+'#')

        data = ser.read(50)
        print 'data : ', data
        print
        


