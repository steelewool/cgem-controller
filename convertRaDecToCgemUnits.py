
# Algorith doesn't handle negavite degrees. Negative angle much be translated
# to be between 270 and 360 degrees.

class RaDecToCgem:
    softwareResolution = 2**24;
    fullCircleDeg      = 360
    fullCircleSec      = fullCircleDeg * 60.0 * 60.0
    
    oneTwelthArcSeconds = fullCircleSec * 12.0
    conversionFactor    = softwareResolution / oneTwelthArcSeconds
    
    def __init__(self, decDeg, decMin, decSec):
        self.decInSeconds =  abs(decDeg) * 60.0 * 60.0 + decMin * 60.0 + decSec
        
        if (decDeg < 0):
            self.decInSeconds = (360.0 * 60.0 * 60.0) - self.decInSeconds;
        
        self.raInSeconds  = (raHr   * 60.0 * 60.0 + raSec  * 60.0 + raSec) * 15.0
#        self.decGotoValue = self.decInSeconds * 12.0 * RaDecToCgem.conversionFactor
#        self.raGotoValue  = self.raInSeconds  * 12.0 * RaDecToCgem.conversionFactor
        self.decGotoValue = convertSeconds(self.decInSeconds)
        self.raGotoValue  = convertSeconds(self.raInSeconds)
        
#        self.decHighByte = int (self.decGotoValue / 256 / 256)
#        self.decMidByte  = int ((self.decGotoValue - (self.decHighByte * 256 * 256)) / 256)
#        self.decLowByte  = int (self.decGotoValue - (self.decHighByte * 256 * 256) - (self.decMidByte * 256))
#        self.raHighByte  = int (self.raGotoValue  / 256 / 256)
#        self.raMidByte   = int ((self.raGotoValue -  (self.raHighByte  * 256 * 256)) / 256)
#        self.raLowByte   = int (self.raGotoValue  - (self.raHighByte  * 256 * 256) - (self.raMidByte  * 256))
        self.decHighByte, self.decMidByte, self.decLowByte = highMidLow(self.decGotoValue)
        self.raHighByte, self.raMidByte, self.raLowByte = highMidLow(self.raGotoValue)
    
    def convertSeconds(seconds):
        return seconds * 12.0 * RaDecToCgem.conversionFactor
    
    def highMidLow(gotoValue):
        highByte = int (gotoValue  / 256 / 256)
        midByte  = int ((gotoValue - (highByte  * 256 * 256)) / 256)
        lowByte  = int (gotoValue  - (highByte  * 256 * 256) - (midByte  * 256))
        return [highByte, midByte, lowByte]

if __name__ == '__main__':
    raHr   = input ('raHr   : ')
    raMin  = input ('raMin  : ')
    raSec  = input ('raSec  : ')
    
    decDeg = input ('decDeg : ')
    decMin = input ('decMin : ')
    decSec = input ('decSec : ')
    
    conversion = RaDecToCgem(decDec, decMin, decSec)
    
    print 'RA   hr min sec      : ', raHr,   ' ', raMin,  ' ', raSec
    print 'Dec deg min sec      : ', decDeg, ' ', decMin, ' ', decSec
    print 'softwareResolution   : ', RaDecToCgem.softwareResolution
    print 'fullCircleSec        : ', RaDecToCgem.fullCircleSec
    print 'oneTwelthArcSeconds  : ', RaDecToCgem.oneTwelthArcSeconds
    print 'conversionFactor     : ', RaDecToCgem.conversionFactor
    print 'decInSeconds         : ', conversion.decInSeconds
    print 'raInSeconds          : ', conversion.raInSeconds
    print 'hex-int decGotoValue : ', hex(int(conversion.decGotoValue))
    print 'hex-int raGotValuie  : ', hex(int(conversion.raGotoValue))
    print 'hex decHighByte      : ', hex(conversion.decHighByte)
    print 'hex decMidByte       : ', hex(conversion.decMidByte)
    print 'hex decLowByte       : ', hex(conversion.decLowByte)
    print 'hex raHighByte       : ', hex(conversion.raHighByte)
    print 'hex raMidByte        : ', hex(conversion.raMidByte)
    print 'hex raLowByte        : ', hex(conversion.raLowByte)

