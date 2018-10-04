import serial
import numpy

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
        self.fromCgem(cgemUnits = ' ')

    # Compute the ra/hex value, store as hex but return as string
    def convertSeconds(self, seconds):
        print 'seconds :', seconds
        self.gotoValue = seconds * 12.0 * CgemConverter.conversionFactor
        print 'self.gotoValue: ', self.gotoValue
        self.hexGotoValue = hex(int(self.gotoValue))
        self.strGotoValue = hex(int(self.gotoValue))[2:]
        x = len(self.strGotoValue)
#        print 'x            : ', x
        addCharacters = 8-x
        print 'strGotoValue : ', self.strGotoValue
        print 'addCharacters: ', addCharacters
        for i in range (0,addCharacters):
            self.strGotoValue += '0'
        print 'self.strGotoValue: ', self.strGotoValue
        return self.strGotoValue

class Ra(CgemConverter):
    hr  = 0.0
    min = 0.0
    sec = 0.0
    raCgemUnits = '0'
    
    def toCgem(self):
        self.raInSeconds     = (self.hr * 60.0 * 60.0 + self.min  * 60.0 + self.sec) * 15.0
        print 'self.raInSeconds: ', self.raInSeconds
        return str.upper(self.convertSeconds(self.raInSeconds))
    
    def fromCgem(self, cgemUnits):
        #x = hex(int(cgemUnits, 16)) >> 8
        #print x
        #print hex(x)
        # lowByte = int(cgemUnits, 16)
        # print 'lowByte: ', lowByte
        return cgemUnits
    
class Dec(CgemConverter):
    deg = 0.0
    min = 0.0
    sec = 0.0
    decCgemUnits = '0'
    
    def toCgem(self):
        self.decInSeconds    =  abs(self.deg) * 60.0 * 60.0 + self.min * 60.0 + self.sec
#        print 'self.decInSeconds: ', self.decInSeconds
        if (self.deg < 0):
            self.decInSeconds = (360.0 * 60.0 * 60.0) - self.decInSeconds;
        
        gotoValue = self.decInSeconds * 12.0 * CgemConverter.conversionFactor
        
#        print 'gotoValue : ', gotoValue
        
        hexGotoValue = hex(int(gotoValue) << 8)
        strGotoValue = str(hexGotoValue)[2:]
        addCharacters = 8-len(strGotoValue)
        for i in range (0,addCharacters):
            strGotoValue += '0'

        return str.upper(strGotoValue)
    
        # return str.upper(self.convertSeconds(self.decInSeconds))

    def fromCgem (self, cgemUnits):
        # y = numpy.uint32(x)
        # x = numpy.uint64 (cgemUnits)
        # lowByte = int(cgemUnits) & 0xFF
        # print x
        # lowByte = x  & 255
        return cgemUnits
# This paradigm was provided by Zach as a way to test the individual
# classes as a main program.

if __name__ == '__main__':
    
    # Is there a better way to initialize the ra and dec values?
    ra = Ra()
    dec = Dec()
    
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
    
    print 'write to the serial: ', 'r' + ra.toCgem() + ',' + dec.toCgem()
    
    raCgemUnits  = ra.toCgem()
    decCgemUnits = dec.toCgem()
    
    print 'raCgemUnits  : ', raCgemUnits
    print 'decCgemUnits : ', decCgemUnits

    print 'RA  fromCgem : ', ra.fromCgem(raCgemUnits)
    print 'Dec fromCgem : ', dec.fromCgem(decCgemUnits)
    
    # worked: print str.upper(str(hex((int(decCgemUnits, 16) >> 8) & 0xff))[2:])
    x = int(decCgemUnits,16) >> 8
    print ' x and hex(x) ', x, hex(x)
    print 'conversionFactor: ', CgemConverter.conversionFactor
    seconds = int(x / 12.0 / CgemConverter.conversionFactor)
    print seconds
    
    