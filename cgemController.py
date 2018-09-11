import convertRaDecToCgemUnits

ra  = convertRaDecToCgemUnits.Ra()
dec = convertRaDecToCgemUnits.Dec()

ra.hr   = input ('raHr   : ')
ra.min  = input ('raMin  : ')
ra.sec  = input ('raSec  : ')
    
dec.deg = input ('decDeg : ')
dec.min = input ('decMin : ')
dec.sec = input ('decSec : ')

x= convertRaDecToCgemUnits.RaDecToCgem (ra.hr,   ra.min,  ra.sec,
                                        dec.deg, dec.min, dec.sec)

print 'ra  : ', ra.hr, ra.min, ra.sec
print 'dec : ', dec.deg, dec.min, dec.sec

# print 'x.strRaGotoValue : ', x.strRaGotoValue

print x.raToCgemUnits (ra)
print x.decToCgemUnits (dec)

print 'r'+x.raToCgemUnits(ra)+','+x.decToCgemUnits(dec)+'#'




