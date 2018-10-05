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
        self.fromCgem(cgemUnits = '0')

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
#        return str.upper(self.convertSeconds(self.raInSeconds))
    
        gotoValue = self.raInSeconds * 12.0 * CgemConverter.conversionFactor
#        print 'gotoValue     : ', gotoValue
#        print 'hex gotoValue : ', hex(int(gotoValue))
        hexGotoValue = hex(int(gotoValue) << 8)
#        print 'hexGotValue << 8: ', hexGotoValue
        strGotoValue = str(hexGotoValue)[2:]
        addCharacters = 8-len(strGotoValue)
        for i in range (0,addCharacters):
            strGotoValue = '0' + strGotoValue
        return str.upper(strGotoValue)

    def fromCgem(self, cgemUnits):
#        print 'Begining of Ra.fromCgem'
#        print 'cgemUnits :', cgemUnits
        x = int(cgemUnits,16)>>8
#        print 'x         : ', x
#        print 'hex x     : ', hex(x)
        seconds = x / 15.0 / 12.0 / CgemConverter.conversionFactor
#        print 'seconds : ', seconds
        hr = int(seconds / 3600.0)
        min = int((seconds - (hr * 3600.0)) / 60.0)
        sec = int(seconds - (hr * 3600.0) - (min * 60.0))
        returnValue = str(hr) + 'h' + str(min) + 'm' + str(sec) + 's'
#        print 'end of Ra.fromCgem'
        return returnValue
    
class Dec(CgemConverter):
    deg = 0.0
    min = 0.0
    sec = 0.0
    decCgemUnits = '0'
    
    def toCgem(self):
#        print 'Dec.toCgem'
        self.decInSeconds    =  abs(self.deg) * 60.0 * 60.0 + self.min * 60.0 + self.sec
#        print 'self.decInSeconds: ', self.decInSeconds
        if (self.deg < 0):
            self.decInSeconds = (360.0 * 60.0 * 60.0) - self.decInSeconds;
        gotoValue = self.decInSeconds * 12.0 * CgemConverter.conversionFactor
#        print 'gotoValue     : ', gotoValue
#        print 'hex gotoValue : ', hex(int(gotoValue))
        hexGotoValue = hex(int(gotoValue) << 8)
#        print 'hexGotValue << 8: ', hexGotoValue
        strGotoValue = str(hexGotoValue)[2:]
        addCharacters = 8-len(strGotoValue)
        for i in range (0,addCharacters):
            strGotoValue = '0' + strGotoValue
#        print 'strGotoValue : ', str.upper(strGotoValue)
#        print 'end of Dec.togem'
        
        return str.upper(strGotoValue)

    def fromCgem (self, cgemUnits):
#        print 'begin Dec.fromCgem'
        x = int(cgemUnits,16) >> 8        
#        print 'cgemUnits      : ', cgemUnits
#        print ' x and hex(x)     : ', x, '   ', hex(x)
#        print 'conversionFactor  : ', CgemConverter.conversionFactor
        seconds = int(x / 12.0 / CgemConverter.conversionFactor)
#        print 'seconds           : ', seconds
        deg = int(seconds / 3600.0)
#        print 'deg               : ', deg
        min = int((seconds - (deg * 3600.0)) / 60.0)
#        print 'min               : ', min
        sec = int(seconds - (deg * 3600.0) - (min * 60.0))
#        print 'sec               : ', sec
#        print 'end Dec.fromCgem'
        
        returnValue = str(deg) + 'd' + str(min) + 'm' + str(sec) + 's'
        return returnValue
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
    
    print 'raCgemUnits    : ', raCgemUnits
    print 'decCgemUnits   : ', decCgemUnits

    print 'Dec fromCgem   : ', dec.fromCgem(decCgemUnits)
    print 'RA  fromCgem   : ', ra.fromCgem(raCgemUnits)