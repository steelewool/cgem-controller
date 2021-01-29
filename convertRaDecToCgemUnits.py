# Pretty sure that having the name Ra and Dec as classes in two different
# modules is confusing me. For now I'm going to prefix Ra and Dec in this
# module with 'Convert'.

# from raDecLst import Ra, Dec, Lst, Alt, Azi
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
    
class CgemConverter(object):

# This is setting up constants for the conversion process:

    softwareResolution = 2**24;
    fullCircleDeg      = 360
    fullCircleSec      = fullCircleDeg * 60.0 * 60.0
    
    oneTwelthArcSeconds = fullCircleSec * 12.0
    conversionFactor    = softwareResolution / oneTwelthArcSeconds

# The for loop below worked in the older version of Python.
# At the current time 1/29/21 I'm not even sure of what this logic
# was supposed to do.

    def __init__(self, args={}):
        #for k,v in args.iteritems():
        #    setattr(self, k, v)
        self.toCgem()
        self.fromCgem(cgemUnits = '0')

# The class CovertRa handles conversion to and from cgem units for
# the RA. The methods defined in the class are:
# __init__
# toCgem
# fromCgem
# getSeconds
# __sub__

class ConvertRa(CgemConverter):
    raCgemUnits = '0'
    
    def __init__ (self, hr=0, min=0, sec=0):
        #args = locals()
        #super(Ra, args.pop('self')).__init__(args)
        self.hr  = hr
        self.min = min
        self.sec = sec
    
    def toCgem(self):
        self.raInSeconds = (float(self.hr) * 3600 + float(self.min)  * 60.0 + float(self.sec)) * 15.0
        
        if int(self.hr) < 0 or int(self.hr) > 23:
            raise RaError.message('hour out of range')
        if int(self.min) < 0 or int(self.min) > 59:
            raise RaError.message('min out of range')
        if float(self.sec) < 0.0 or float(self.sec) > 59.99:
            raise RaError.message('sec out of range')
        if float(self.raInSeconds) < 0.0:
            raise RaError.message('seconds less than 0')
        if float(self.raInSeconds) >= 86400*15.0:
            raise RaError.message('seconds > 86400 seconds')

        gotoValue = self.raInSeconds * 12.0 * CgemConverter.conversionFactor
        hexGotoValue = hex(int(gotoValue) << 8)
        strGotoValue = str(hexGotoValue)[2:]
        addCharacters = 8-len(strGotoValue)

        for i in range (0,addCharacters):
            strGotoValue = '0' + strGotoValue

        return str.upper(strGotoValue)

    def fromCgem(self, cgemUnits):
        x = (int(cgemUnits,16)) >> 8
        seconds = x / 15.0 / 12.0 / CgemConverter.conversionFactor
        xhr = int(seconds / 3600.0)
        xmin = int((seconds - (xhr * 3600.0)) / 60.0)
        xsec = int(seconds - (xhr * 3600.0) - (xmin * 60.0))
        returnValue = str(xhr) + 'h' + str(xmin) + 'm' + str(xsec) + 's'
        return [xhr, xmin, xsec]

    def getSeconds(self):
        return ((float(self.hr )   * 3600.0) +
                (float(self.min)   *   60.0) +
                (float(self.sec))) *   15.0

    # define subtracttion

    def __sub__ (self, y):
        xSeconds = self.getSeconds()
        ySeconds = y.getSeconds()
        return xSeconds - ySeconds
    
# The class CovertDec handles conversion to and from cgem units for
# the Dec. The methods defined in the class are:
# __init__
# toCgem
# fromCgem
# getSeconds
# __lt__
# __le__
# __eq__

class ConvertDec(CgemConverter):
    decCgemUnits = '0'
    
    def __init__ (self, deg=0, min=0, sec=0):
        self.deg = deg
        self.min = min
        self.sec = sec
        
    def toCgem(self):
        decNeg = False;
        
        if int(self.deg) < 0:
            decNeg = True
            self.deg = -self.deg

        if int(self.deg) > 90 or int(self.deg) < -90:
            raise DecError.message('deg out of range')
        if int(self.min) < 0:
            decNeg = True
            self.min = -int(self.min)
        if int(self.min) < 0 or int(self.min) >= 60:
            raise DecError.msg('min out of range')
        if int(self.sec) < 0:
            decNeg = True
            self.sec = -int(self.sec)
        if  int(self.sec) < 0 or int(self.sec) >= 60:
            raise DecError.msg('sec out of range')

        self.decInSeconds    =  abs(float(self.deg)) * 60.0 * 60.0 + float(self.min) * 60.0 + float(self.sec)

        if decNeg:
            self.decInSeconds = (360.0 * 60.0 * 60.0) - float(self.decInSeconds)

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

        if seconds > 180.0*60.0*60.0:
            seconds = seconds - (360.0*60.0*60.0)
        xdeg = int(seconds / 3600.0)
        xmin = int((seconds - (xdeg * 3600.0)) / 60.0)
        xsec = int(seconds - (xdeg * 3600.0) - (xmin * 60.0))
        returnValue = str(xdeg) + 'd' + str(xmin) + 'm' + str(xsec) + 's'
        return [xdeg, xmin, xsec]
    
    def getSeconds(self):
        return (float(self.deg) * 60.0 * 60.0) + (float(self.min)  * 60.0) + float(self.sec)

    def __lt__ (self,y):
        return self.getSeconds() < y.getSeconds()

    def __le__ (self,y):
        return self.getSeconds() <= y.getSeconds()

    def __eq__ (self,y):
        return self.getSeconds() == y.getSeconds()

# The class CovertLst handles conversion to seconds.
# The methods defined in the class are:
# __init__
# getSeconds
# __sub__

class ConvertLst:
    def __init__ (self, hr = 0, min = 0, sec = 0.0):
        self.hr  = hr
        self.min = min
        self.sec = sec

    def getSeconds(self):
        return ((self.hr * 60.0 * 60.0) + (self.min * 60.0) + self.sec) * 15.0

    # define subtracttion
    def __sub__ (self, y):
        xSeconds = self.getSeconds()
        ySeconds = y.getSeconds()
        return xSeconds - ySeconds

# The class CovertAlt handles conversions to sectonds.
# The methods defined in the class are:
# __init__
# getSeconds

class ConvertAlt:
    def __init__ (self, deg = 0.0):
        self.deg = deg
    def getSeconds(self):
        return (float(self.deg) * 60.0 * 60.0)
    
# The class CovertAzi handles conversions to sectonds.
# The methods defined in the class are:
# __init__
# getSeconds

class ConvertAzi:
    def __init__ (self, deg = 0.0):
        self.deg = deg

    def getSeconds(self):
        return (float(self.deg) * 60.0 * 60.0)

if __name__ == '__main__':
    
    # Is there a better way to initialize the ra and dec values?
    
    #hr   = input ('raHr   : ')
    #min  = input ('raMin  : ')
    #sec  = input ('raSec  : ')

    #ra = ConvertRa(hr, min, sec)

    ra  = ConvertRa  ('18', '45', '41') # seconds were 40.8
    dec = ConvertDec ('41', '15', '58')
    
    print ('RA   hr min sec      : ', ra.hr,   ' ', ra.min,  ' ', ra.sec)
    print ('Dec deg min sec      : ', dec.deg, ' ', dec.min, ' ', dec.sec)
    
    try:
        raCgemUnits  = ra.toCgem()
        print ('raCgemUnits    : ', raCgemUnits)
        print ('RA  fromCgem   : ', ra.fromCgem(raCgemUnits))
    except:
        print ('ra.toCgem failed')

    try:
        decCgemUnits = dec.toCgem()
        print ('decCgemUnits   : ', decCgemUnits)
        print ('Dec fromCgem   : ', dec.fromCgem(decCgemUnits))
    except:
        print ('dec.toCgem failed')

    
    print ('Doing a translation to RA/Dec from numbers from telescope')
    
    cgemRa  = 'C78DC600'
    cgemDec = '1C6B1D00'
    
    print ('cgemRa, cgemDec: ', cgemRa, cgemDec)

    print ('RA : ', ra.fromCgem(cgemRa))
    print ('Dec: ', dec.fromCgem(cgemDec))

    print ()
    print ()
    
    cgemRa  = 'C81F1900'
    cgemDec = '1D584400'
    
    print ('cgemRa, cgemDec: ', cgemRa, cgemDec)

    print ('RA : ', ra.fromCgem(cgemRa))
    print ('Dec: ', dec.fromCgem(cgemDec))

#    print ('RA   hr min sec: ', CovertRa.fromCgem(cgemRa))
#    print ('Dec deg min sec: ', Dec.fromCgem(cgemDec))

    ra  = ConvertRa  ('03', '20', '00')
    dec = ConvertDec ('00', '00', '00')
    
    print ('RA   hr min sec      : ', ra.hr,   ' ', ra.min,  ' ', ra.sec)
    print ('Dec deg min sec      : ', dec.deg, ' ', dec.min, ' ', dec.sec)
    
    try:
        raCgemUnits  = ra.toCgem()
        print ('raCgemUnits    : ', raCgemUnits)
        print ('RA  fromCgem   : ', ra.fromCgem(raCgemUnits))
    except:
        print ('ra.toCgem failed')

    try:
        decCgemUnits = dec.toCgem()
        print ('decCgemUnits   : ', decCgemUnits)
        print ('Dec fromCgem   : ', dec.fromCgem(decCgemUnits))
    except:
        print ('dec.toCgem failed')

    print ()
    print ()
    
    ra  = ConvertRa  ('03', '20', '00')
    dec = ConvertDec ('45', '00', '00')
    
    print ('RA   hr min sec      : ', ra.hr,   ' ', ra.min,  ' ', ra.sec)
    print ('Dec deg min sec      : ', dec.deg, ' ', dec.min, ' ', dec.sec)

    try:
        raCgemUnits  = ra.toCgem()
        print ('raCgemUnits    : ', raCgemUnits)
        print ('RA  fromCgem   : ', ra.fromCgem(raCgemUnits))
    except:
        print ('ra.toCgem failed')

    try:
        decCgemUnits = dec.toCgem()
        print ('decCgemUnits   : ', decCgemUnits)
        print ('Dec fromCgem   : ', dec.fromCgem(decCgemUnits))
    except:
        print ('dec.toCgem failed')

    print ()
    print ()
    
    ra  = ConvertRa  ('06', '00', '00')
    dec = ConvertDec ('00', '00', '00')
    
    print ('RA   hr min sec      : ', ra.hr,   ' ', ra.min,  ' ', ra.sec)
    print ('Dec deg min sec      : ', dec.deg, ' ', dec.min, ' ', dec.sec)

    try:
        raCgemUnits  = ra.toCgem()
        print ('raCgemUnits    : ', raCgemUnits)
        print ('RA  fromCgem   : ', ra.fromCgem(raCgemUnits))
    except:
        print ('ra.toCgem failed')

    try:
        decCgemUnits = dec.toCgem()
        print ('decCgemUnits   : ', decCgemUnits)
        print ('Dec fromCgem   : ', dec.fromCgem(decCgemUnits))
    except:
        print ('dec.toCgem failed')

    print ()
    print ()
    
    ra  = ConvertRa  ('09', '00', '00')
    dec = ConvertDec ('00', '00', '00')
    
    print ('RA   hr min sec      : ', ra.hr,   ' ', ra.min,  ' ', ra.sec)
    print ('Dec deg min sec      : ', dec.deg, ' ', dec.min, ' ', dec.sec)

    try:
        raCgemUnits  = ra.toCgem()
        print ('raCgemUnits    : ', raCgemUnits)
        print ('RA  fromCgem   : ', ra.fromCgem(raCgemUnits))
    except:
        print ('ra.toCgem failed')

    try:
        decCgemUnits = dec.toCgem()
        print ('decCgemUnits   : ', decCgemUnits)
        print ('Dec fromCgem   : ', dec.fromCgem(decCgemUnits))
    except:
        print ('dec.toCgem failed')

    print ()
    print ()
    
    cgemRa  = '238E7C00'
    cgemDec = '00033900'
    
    print ('cgemRa, cgemDec: ', cgemRa, cgemDec)

    print ('RA : ', ra.fromCgem(cgemRa))
    print ('Dec: ', dec.fromCgem(cgemDec))

    print ()
    print ()

    cgemRa  = '238F5B00'
    cgemDec = '20012000'
    
    print ('cgemRa, cgemDec: ', cgemRa, cgemDec)

    print ('RA : ', ra.fromCgem(cgemRa))
    print ('Dec: ', dec.fromCgem(cgemDec))

    print ()
    print ()

    cgemRa  = '5553B000'
    cgemDec = 'F8E12600'
    
    print ('cgemRa, cgemDec: ', cgemRa, cgemDec)

    print ('RA : ', ra.fromCgem(cgemRa))
    print ('Dec: ', dec.fromCgem(cgemDec))

    print ()
    print ()

    ra  = ConvertRa  ('08', '00', '00')
    dec = ConvertDec ('10', '00', '00')
    
    print ('RA   hr min sec      : ', ra.hr,   ' ', ra.min,  ' ', ra.sec)
    print ('Dec deg min sec      : ', dec.deg, ' ', dec.min, ' ', dec.sec)

    try:
        raCgemUnits  = ra.toCgem()
        print ('raCgemUnits    : ', raCgemUnits)
        print ('RA  fromCgem   : ', ra.fromCgem(raCgemUnits))
    except:
        print ('ra.toCgem failed')

    try:
        decCgemUnits = dec.toCgem()
        print ('decCgemUnits   : ', decCgemUnits)
        print ('Dec fromCgem   : ', dec.fromCgem(decCgemUnits))
    except:
        print ('dec.toCgem failed')

    print ()
    print ()

    raHex       = b'C7582100'
    raFromCgem  = ra.fromCgem(raHex)
    print ('raFromCgem: ', raFromCgem)

    decHex      = b'1C761C00'
    decFromCgem = dec.fromCgem(decHex)
    print ('decFromCgem: ', decFromCgem)


