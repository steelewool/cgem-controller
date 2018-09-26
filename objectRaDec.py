# The class ObjectRaDec, which is not a very description name is
# intended to provide sorting of a list of objects for the 'best'
# observing order.

# As of 9/25/18 I have the LST embedded in the ObjectRaDec object. It may make more
# sense to place in the list - but but is still a deferred design detail.

class Ra:
    def __init__ (self, hr = 0, min = 0, sec = 0):
        self.hr  = hr
        self.min = min
        self.sec = sec
    def getSeconds(self):
        return ((self.hr * 60.0 * 60.0) + (self.min  * 60.0) + self.sec) * 15.0
    # define subtracttion
    def __sub__ (self, y):
        xSeconds = self.getSeconds()
        ySeconds = y.getSeconds()
        return xSeconds - ySeconds
    
class Dec():
    def __init__ (self, deg = 0, min = 0, sec = 0):
        self.deg = deg
        self.min = min
        self.sec = sec
    def getSeconds(self):
        return (self.deg * 60.0 * 60.0) + (self.min  * 60.0) + self.sec

class Lst:
    def __init__ (self, hr = 0, min = 0, sec = 0):
        self.hr  = hr
        self.min = min
        self.sec = sec
    def getSeconds(self):
        return ((self.hr * 60.0 * 60.0) + (self.min * 60.0) + self.sec) * 15.0

class ObjectRaDec:
    def __init__ (self, ra = Ra(), dec = Dec(), lst = Lst()):
        self.ra  = ra
        self.dec = dec
        self.lst = lst

# Need to look up the formula for computing local hour angle. This subtraction
# could be reversed.
# Zach - why does the subtraction of a ra and lst work. I would have thought I
#        needed a cast operator.

    def localHrAngle(self):
        return int((self.ra - self.lst)/(3600*15))

    # This function will the bin value for searching and sorting. 
    def bin (self):
        if (self.dec.deg > 70):
            return 1
        else:
            localHrAngle = self.localHrAngle()
            if (localHrAngle > 0):
                return 2
            else:
                return 3

# First determine which bin the two objects are in which is based on the LST.

    # define == operator
    def __eq__ (x,y):
        if ((x.ra == y.ra) and (x.dec == y.dec)):
            return 1
        else:
            return 0

    # define < operation for 
    def __lt__ (x,y):
        xRaInSeconds  = x.ra.getSeconds()
        yRaInSeconds  = y.ra.getSeconds()
        xDecInSeconds = x.dec.getSeconds()
        yDecInSeconds = y.dec.getSeconds()

        print xRaInSeconds
        print yRaInSeconds
        print xDecInSeconds
        print yDecInSeconds
        return 0

# If the objects declination is > 70 degrees north then it goes in bin 1. The other 12 bins start
# with the local angle of -90 degree going each by 15 degree increments until I get to +90 degree.

# Yet another questions, whey am I having to use getLst() instead of lst?
        
    def write(self):
        print '   RA   hr min sec: ' + str(self.ra.hr)   + ':' + str(self.ra.min)  + ':' + str(self.ra.sec)
        print '   Dec deg min sec: ' + str(self.dec.deg) + ':' + str(self.dec.min) + ':' + str(self.ra.sec)
        print '   LST  hr min sec: ' + str(self.lst.hr)  + ':' + str(self.lst.min) + ':' + str(self.lst.sec)
        print

# Using the paradigm supplied by Zach to be able to test this class

if __name__ == '__main__':

    import astropy.time
    from   astropy.time        import Time
    from   astropy             import units as u
    from   astropy.coordinates import EarthLocation
    from   astropy.coordinates import SkyCoord

    observingPosition = EarthLocation(lat    = (34+49/60+32/3600) *u.deg,
                                      lon    =-(118+1/60+27*3600) *u.deg,
                                      height = (5000 * 0.3048)    *u.m)
    
    print 'observingPosition            : ', observingPosition
    print 'astropy.time.Time.now()      : ', astropy.time.Time.now()

    date = astropy.time.Time(astropy.time.Time.now(),
                             scale='utc',
                             location=observingPosition)
    
    print 'date                         : ', date
    print 'date.now()                   : ', date.now()
    print 'date.sidereal_time(mean)     : ', date.sidereal_time('mean')
    print 'date.sidereal_time(apparent) : ', date.sidereal_time('apparent')

    meanLST = date.sidereal_time('mean')
    print 'meanLST                      : ', meanLST
    
    print '----------------------'  
    
    object1 = ObjectRaDec(Ra(12,13,14),Dec(1,2,3), Lst(4,5,6))
    object2 = ObjectRaDec(Ra(0,1,2),   Dec(3,4,5), Lst(6,7,8))
    object3 = object2

    object1.write()
    object2.write()
    object3.write()
    
    print 'subtract ra  : ', object1.ra - object2.ra
    print 'localHrAngle : ', object1.localHrAngle()
    print 'bin          : ', object1.bin()
    
    print 'testing == operator'
    
    if (object3 == object2):
        print 'equal is True'
    else:
        print 'equal is False'

    if (object1 < object2):
        print 'less than true'
    else:
        print 'less than false'
