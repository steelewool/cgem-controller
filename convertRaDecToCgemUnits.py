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

    # Compute the ra/hex value, store as hex but return as string
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

# Zach, how would I structure this object to be able to be initialized with
#       a RA and Declination.

class ObjectRaDec():
    ra  = Ra()
    dec = Dec()

#   lst = Ra(12.0,15.0,3.0)
    lst = Ra()
    lst.hr  = 15
    lst.min = 10
    lst.sec = 0

# First determine which bin the two objects are in which is based on the LST.

    def __eq__ (x,y):
        if ((x.ra == y.ra) and (x.dec == y.dec)):
            return 0
        else:
            return -1;

    def __lt__ (x,y):

        xRaInSeconds  = ((x.ra.hr   * 60.0 * 60.0) + (x.ra.min  * 60.0) + x.ra.sec) * 15.0
        yRaInSeconds  = ((y.ra.hr   * 60.0 * 60.0) + (y.ra.min  * 60.0) + y.ra.sec) * 15.0
        xDecInSeconds =  (x.dec.deg * 60.0 * 60.0) + (x.dec.min * 60.0) + x.dec.sec
        yDecInSeconds =  (y.dec.deg * 60.0 * 60.0) + (y.dec.min * 60.0) + y.dec.sec

        if (x.dec.deg > 70):
            xBin = 1
        else:
            print 'need code to computer xBin'
            
        return 0

if __name__ == '__main__':
    ra  = Ra()
    dec = Dec()

    object1 = ObjectRaDec()
    object2 = ObjectRaDec()

    object1.ra.hr   = 10
    object1.dec.deg =  0
    object2.ra.hr   = 15
    object2.dec.deg =  0

    if (object1 == object2):
        print 'equal is True'
    else:
        print 'equal to False'

    if (object1 < object2):
        print 'less than true'
    else:
        print 'less than false'
        
    ra.hr   = input ('raHr   : ')
    ra.min  = input ('raMin  : ')
    ra.sec  = input ('raSec  : ')
    
    dec.deg = input ('decDeg : ')
    dec.min = input ('decMin : ')
    dec.sec = input ('decSec : ')

    print 'RA   hr min sec      : ', ra.hr,   ' ', ra.min,  ' ', ra.sec
    print 'Dec deg min sec      : ', dec.deg, ' ', dec.min, ' ', dec.sec
    print 'softwareResolution   : ', CgemConverter.softwareResolution
    print 'fullCircleSec        : ', CgemConverter.fullCircleSec
    print 'oneTwelthArcSeconds  : ', CgemConverter.oneTwelthArcSeconds
    print 'conversionFactor     : ', CgemConverter.conversionFactor

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

