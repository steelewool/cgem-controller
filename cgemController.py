import convertRaDecToCgemUnits

ra  = convertRaDecToCgemUnits.Ra()
dec = convertRaDecToCgemUnits.Dec()

# Zach, is there a cleaner way to do this?

x = convertRaDecToCgemUnits.RaDecToCgem()

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

        print 'r'+x.raToCgemUnits(ra)+','+x.decToCgemUnits(dec)+'#'








