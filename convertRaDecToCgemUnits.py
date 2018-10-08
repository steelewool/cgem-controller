import serial

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class RaError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg  = msg

class DecError(Error):
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg  = msg
    
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

class Ra(CgemConverter):
    hr  = 0.0
    min = 0.0
    sec = 0.0
    raCgemUnits = '0'
    
    def __init__ (self, hr=0, min=0, sec=0):
        self.hr = hr
        self.min = min
        self.sec = sec
        
    def toCgem(self):
        self.raInSeconds = (self.hr * 60.0 * 60.0 + self.min  * 60.0 + self.sec) * 15.0
        if self.hr < 0 or self.hr > 23:
            print 'hr is out of range'
            raise RaError.message('hour out of range')
        if self.min < 0 or self.min > 59:
            print 'min is out of range'
            raise RaError.message('min out of range')
        if self.sec < 0 or self.sec > 59:
            print 'sec is out of range'
            raise RaError.message('sec out of range')
        if self.raInSeconds < 0:
            print 'ra is less than 0'
            raise RaError.message('seconds less than 0')
        if self.raInSeconds >= 86400*15.0:
            print 'ra is greater than 24 hours'   
            raise RaError.message('seconds > 86400 seconds')
        gotoValue = self.raInSeconds * 12.0 * CgemConverter.conversionFactor
        hexGotoValue = hex(int(gotoValue) << 8)
        strGotoValue = str(hexGotoValue)[2:]
        addCharacters = 8-len(strGotoValue)
        for i in range (0,addCharacters):
            strGotoValue = '0' + strGotoValue
        return str.upper(strGotoValue)

    def fromCgem(self, cgemUnits):
        x = int(cgemUnits,16)>>8
        seconds = x / 15.0 / 12.0 / CgemConverter.conversionFactor
        self.hr = int(seconds / 3600.0)
        self.min = int((seconds - (self.hr * 3600.0)) / 60.0)
        self.sec = int(seconds - (self.hr * 3600.0) - (self.min * 60.0))
        returnValue = str(self.hr) + 'h' + str(self.min) + 'm' + str(self.sec) + 's'
        return [self.hr, self.min, self.sec]
    
class Dec(CgemConverter):
    deg = 0.0
    min = 0.0
    sec = 0.0
    decCgemUnits = '0'
    
    def __init__ (self, deg=0, min=0, sec=0):
        self.deg = deg
        self.min = min
        self.sec = sec
        
    def toCgem(self):
        if self.deg > 90 or self.deg < -90:
            raise DecError.message('deg out of range')
        if self.min < 0 or self.min > 59:
            raise DecError.msg('min out of range')
        if  self.sec < 0 or self.sec > 59:
            raise DecError.msg('sec out of range')
        self.decInSeconds    =  abs(self.deg) * 60.0 * 60.0 + self.min * 60.0 + self.sec
        if (self.deg < 0):
            self.decInSeconds = (360.0 * 60.0 * 60.0) - self.decInSeconds;
        gotoValue = self.decInSeconds * 12.0 * CgemConverter.conversionFactor
        hexGotoValue = hex(int(gotoValue) << 8)
        strGotoValue = str(hexGotoValue)[2:]
        addCharacters = 8-len(strGotoValue)
        for i in range (0,addCharacters):
            strGotoValue = '0' + strGotoValue       
        return str.upper(strGotoValue)

    def fromCgem (self, cgemUnits):
        x = int(cgemUnits,16) >> 8        
        seconds = int(x / 12.0 / CgemConverter.conversionFactor)
        self.deg = int(seconds / 3600.0)
        self.min = int((seconds - (self.deg * 3600.0)) / 60.0)
        self.sec = int(seconds - (self.deg * 3600.0) - (self.min * 60.0))
        returnValue = str(self.deg) + 'd' + str(self.min) + 'm' + str(self.sec) + 's'
        return [self.deg, self.min, self.sec]

if __name__ == '__main__':
    
    # Is there a better way to initialize the ra and dec values?
    
    hr   = input ('raHr   : ')
    min  = input ('raMin  : ')
    sec  = input ('raSec  : ')
    
    ra = Ra(hr, min, sec)
    
    deg = input ('decDeg : ')
    min = input ('decMin : ')
    sec = input ('decSec : ')
    
    dec = Dec (deg, min, sec)
    
    print 'RA   hr min sec      : ', ra.hr,   ' ', ra.min,  ' ', ra.sec
    print 'Dec deg min sec      : ', dec.deg, ' ', dec.min, ' ', dec.sec
    
    try:
        print 'write to the serial: ', 'r' + ra.toCgem() + ',' + dec.toCgem()
    except:
        print 'failure in conversion to cgem'
        
    try:
        raCgemUnits  = ra.toCgem()
        print 'raCgemUnits    : ', raCgemUnits
        print 'RA  fromCgem   : ', ra.fromCgem(raCgemUnits)
    except:
        print 'ra.toCgem failed'

    try:
        decCgemUnits = dec.toCgem()
        print 'decCgemUnits   : ', decCgemUnits
        print 'Dec fromCgem   : ', dec.fromCgem(decCgemUnits)
    except:
        print 'dec.toCgem failed'
