
raHr   =   1.0
raMin  =   1.0
raSec  =   1.0

decDeg = -45.0
decMin =  30.0
decSec =   0.0

# Algorith doesn't handle negavite degrees. Negative angle much be translated
# to be between 270 and 360 degrees.

softwareResolution = 2**24;
fullCircleDeg      = 360
fullCircleSec      = fullCircleDeg * 60.0 * 60.0

oneTwelthArcSeconds = fullCircleSec * 12.0
conversionFactor    = softwareResolution / oneTwelthArcSeconds

decInSeconds =  abs(decDeg) * 60.0 * 60.0 + decMin * 60.0 + decSec

if (decDeg < 0):
    decInSeconds = (360.0 * 60.0 * 60.0) - decInSeconds;
    
raInSeconds  = (raHr   * 60.0 * 60.0 + raSec  * 60.0 + raSec) * 15.0

decGotoValue = decInSeconds * 12.0 * conversionFactor
raGotoValue  = raInSeconds  * 12.0 * conversionFactor

decHighByte = int (decGotoValue / 256 / 256)
decMidByte  = int ((decGotoValue - (decHighByte * 256 * 256)) / 256)
decLowByte  = int (decGotoValue - (decHighByte * 256 * 256) - (decMidByte * 256))

raHighByte  = int (raGotoValue  / 256 / 256)
raMidByte   = int ((raGotoValue -  (raHighByte  * 256 * 256)) / 256)
raLowByte   = int (raGotoValue  - (raHighByte  * 256 * 256) - (raMidByte  * 256))

print 'RA   hr min sec      : ', raHr,   ' ', raMin,  ' ', raSec
print 'Dec deg min sec      : ', decDeg, ' ', decMin, ' ', decSec
print 'softwareResolution   : ', softwareResolution
print 'fullCircleSec        : ', fullCircleSec
print 'oneTwelthArcSeconds  : ', oneTwelthArcSeconds
print 'conversionFactor     : ', conversionFactor
print 'decInSeconds         : ', decInSeconds
print 'raInSeconds          : ', raInSeconds
print 'hex-int decGotoValue : ', hex(int(decGotoValue))
print 'hex-int raGotValuie  : ', hex(int(raGotoValue))
print 'hex decHighByte      : ', hex(decHighByte)
print 'hex decMidByte       : ', hex(decMidByte)
print 'hex decLowByte       : ', hex(decLowByte)
print 'hex raHighByte       : ', hex(raHighByte)
print 'hex raMidByte        : ', hex(raMidByte)
print 'hex raLowByte        : ', hex(raLowByte)


