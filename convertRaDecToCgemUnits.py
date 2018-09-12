import serial

    
# Algorith doesn't handle negavite degrees. Negative angle much be translated
# to be between 270 and 360 degrees.

class CgemConverter:

# This is setting up constants for the conversion process:

    softwareResolution = 2**24;
    fullCircleDeg      = 360
    fullCircleSec      = fullCircleDeg * 60.0 * 60.0
    
    oneTwelthArcSeconds = fullCircleSec * 12.0
    conversionFactor    = softwareResolution / oneTwelthArcSeconds

    # This only works when instantiating child classes (Ra and Dec)
    def __init__(self):
        self.toCgem()

    # Compute the ra/hex value
    def convertSeconds(self, seconds):
        self.gotoValue = seconds * 12.0 * CgemConverter.conversionFactor
        self.hexGotoValue = hex(int(self.gotoValue))
        self.strGotoValue = hex(int(self.gotoValue))[2:]
        return self.strGotoValue

# Function may be deprecated after things are working.

    def highMidLow(self, gotoValue):
        highByte = int (gotoValue  / 256 / 256)
        midByte  = int ((gotoValue - (highByte  * 256 * 256)) / 256)
        lowByte  = int (gotoValue  - (highByte  * 256 * 256) - (midByte  * 256))
        return [highByte, midByte, lowByte]

class Ra(CgemConverter):
    hr  = 0.0
    min = 0.0
    sec = 0.0
    
    def toCgem(self):
        self.raInSeconds     = (self.hr * 60.0 * 60.0 + self.min  * 60.0 + self.sec) * 15.0
        return self.convertSeconds(self.raInSeconds)

class Dec(CgemConverter):
    deg = 0.0
    min = 0.0
    sec = 0.0
    
    def toCgem(self):
        self.decInSeconds    =  abs(self.deg) * 60.0 * 60.0 + self.min * 60.0 + self.sec
        
        if (self.deg < 0):
            self.decInSeconds = (360.0 * 60.0 * 60.0) - self.decInSeconds;
        
        return self.convertSeconds(self.decInSeconds)

if __name__ == '__main__':
    ra = Ra()
    dec = Dec()
    
    ra.hr   = input ('raHr   : ')
    ra.min  = input ('raMin  : ')
    ra.sec  = input ('raSec  : ')
    
    dec.deg = input ('decDeg : ')
    dec.min = input ('decMin : ')
    dec.sec = input ('decSec : ')

    conversion = CgemConverter()
    
    print 'RA   hr min sec      : ', ra.hr,   ' ', ra.min,  ' ', ra.sec
    print 'Dec deg min sec      : ', dec.deg, ' ', dec.min, ' ', dec.sec
    print 'softwareResolution   : ', CgemConverter.softwareResolution
    print 'fullCircleSec        : ', CgemConverter.fullCircleSec
    print 'oneTwelthArcSeconds  : ', CgemConverter.oneTwelthArcSeconds
    print 'conversionFactor     : ', CgemConverter.conversionFactor
#    print 'decInSeconds         : ', self.decInSeconds
#    print 'raInSeconds          : ', self.raInSeconds
#    print 'hex-int decGotoValue : ', hex(int(conversion.decGotoValue))
#    print 'hex-int raGotValuie  : ', hex(int(conversion.raGotoValue))
#    print 'hex decHighByte      : ', hex(conversion.decHighByte)
#    print 'hex decMidByte       : ', hex(conversion.decMidByte)
#    print 'hex decLowByte       : ', hex(conversion.decLowByte)
#    print 'hex raHighByte       : ', hex(conversion.raHighByte)
#    print 'hex raMidByte        : ', hex(conversion.raMidByte)
#    print 'hex raLowByte        : ', hex(conversion.raLowByte)

# This fails if there is no serial device. Need someway to test without the
# hardware being present. Until then I'll put a #@ in front of serial
# commands until I get this resolved

#@    ser = serial.Serial('/dev/ttyUSB0', timeout=1)
    
#@    print 'ser name : ', ser.name

    print 'write to the serial: ', 'r' + ra.toCgem() + ',' + dec.toCgem()
    
#@    ser.write ('r' + conversion.strRaGotoValue + ',' + conversion.strDecGotoValue)
    
#@    char = ser.read(100)
    
#@    print 'char     : ', char

    raCgemUnits  = ra.toCgem()
    decCgemUnits = dec.toCgem()
    
    print 'raCgemUnits  : ', raCgemUnits
    print 'decCgemUnits : ', decCgemUnits
    
#@    ser.close()

