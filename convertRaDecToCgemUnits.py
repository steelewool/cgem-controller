import serial
    
# Algorith doesn't handle negavite degrees. Negative angle much be translated
# to be between 270 and 360 degrees.

class Ra:
    hr  = 0.0
    min = 0.0
    sec = 0.0

class Dec:
    deg = 0.0
    min = 0.0
    sec = 0.0


class RaDecToCgem:

    ra  = Ra()
    dec = Dec()

# This is setting up constants for the conversion process:

    softwareResolution = 2**24;
    fullCircleDeg      = 360
    fullCircleSec      = fullCircleDeg * 60.0 * 60.0
    
    oneTwelthArcSeconds = fullCircleSec * 12.0
    conversionFactor    = softwareResolution / oneTwelthArcSeconds

# This function is doing the conversion of RA and Declination to
# cgem units.

    def __init__(self, raHr, raMin, raSec, decDeg, decMin, decSec):
        self.decInSeconds =  abs(decDeg) * 60.0 * 60.0 + decMin * 60.0 + decSec
        
        if (decDeg < 0):
            self.decInSeconds = (360.0 * 60.0 * 60.0) - self.decInSeconds;
        
        self.raInSeconds  = (raHr * 60.0 * 60.0 + raSec  * 60.0 + raSec) * 15.0
        
        self.decGotoValue = self.convertSeconds(self.decInSeconds)
        self.raGotoValue  = self.convertSeconds(self.raInSeconds)
        
        self.hexDecGotoValue = hex(int(self.decGotoValue))
        self.hexRaGotoValue  = hex(int(self.raGotoValue))
        
        self.strDecGotoValue = hex(int(self.decGotoValue))[2:]
        self.strRaGotoValue  = hex(int(self.raGotoValue))[2:]

# the function highMidLow isn't really necessary any longer and should
# be depricated after I'm sure everthing is working correctly.

        self.decHighByte, self.decMidByte, self.decLowByte = self.highMidLow(self.decGotoValue)
        self.raHighByte, self.raMidByte, self.raLowByte = self.highMidLow(self.raGotoValue)

        print self.strRaGotoValue, ',', self.strDecGotoValue

    def raToCgemUnits (self, ra):
        self.raInSeconds  = (ra.hr * 60.0 * 60.0 + ra.min  * 60.0 + ra.sec) * 15.0
        
        self.raGotoValue  = self.convertSeconds(self.raInSeconds)
        self.hexRaGotoValue  = hex(int(self.raGotoValue))
        self.strRaGotoValue  = hex(int(self.raGotoValue))[2:]
        return self.strRaGotoValue
    
    def decToCgemUnits (self, dec):
        self.decInSeconds =  abs(dec.deg) * 60.0 * 60.0 + dec.min * 60.0 + dec.sec
        
        if (dec.deg < 0):
            self.decInSeconds = (360.0 * 60.0 * 60.0) - self.decInSeconds;
        
        self.decGotoValue    = self.convertSeconds(self.decInSeconds)
        self.hexDecGotoValue = hex(int(self.decGotoValue))
        self.strDecGotoValue = hex(int(self.decGotoValue))[2:]
        return self.strDecGotoValue

    def convertSeconds(self, seconds):
        return seconds * 12.0 * RaDecToCgem.conversionFactor

# Function may be depricated after things are working.

    def highMidLow(self, gotoValue):
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
    
    conversion = RaDecToCgem(raHr, raMin, raSec, decDeg, decMin, decSec)
    
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

# This fails if there is no serial device. Need someway to test without the
# hardware being present. Until then I'll put a #@ in front of serial
# commands until I get this resolved

#@    ser = serial.Serial('/dev/ttyUSB0', timeout=1)
    
#@    print 'ser name : ', ser.name

    print 'write to the serial: ', 'r' + conversion.strRaGotoValue + ',' + conversion.strDecGotoValue
    
#@    ser.write ('r' + conversion.strRaGotoValue + ',' + conversion.strDecGotoValue)
    
#@    char = ser.read(100)
    
#@    print 'char     : ', char

    ra  = Ra()
    dec = Dec()
    
    ra.hr = 12

    raCgemUnits  = conversion.raToCgemUnits(ra)
    decCgemUnits = conversion.decToCgemUnits(dec)
    
    print 'raCgemUnits  : ', raCgemUnits
    print 'decCgemUnits : ', decCgemUnits
    
#@    ser.close()

