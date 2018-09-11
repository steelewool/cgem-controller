import convertRaDecToCgemUnits

raHr   = input ('raHr   : ')
raMin  = input ('raMin  : ')
raSec  = input ('raSec  : ')
    
decDeg = input ('decDeg : ')
decMin = input ('decMin : ')
decSec = input ('decSec : ')

convertRaDecToCgemUnits.RaDecToCgem (raHr, raMin, raSec,
                                     decDeg, decMin, decSec)


