# The class ObjectRaDec, which is not a very description name is
# intended to provide sorting of a list of objects for the 'best'
# observing order.

# Not sure where this from came from - uness LiClipse added it.

from pyraf.iraffunctions import substr

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
        return (float(self.deg) * 60.0 * 60.0) + (float(self.min)  * 60.0) + float(self.sec)
    def __lt__ (self,y):
        return self.getSeconds() < y.getSeconds()
    def __le__ (self,y):
        return self.getSeconds() <= y.getSeconds()
    def __eq__ (self,y):
        return self.getSeconds() == y.getSeconds()

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

    # This function will the bin value for searching and sorting. #
    # Bin  1 is for objects north of 70 degrees declination
    # Bin  2 is for LHA -6
    # Bin  3 is for LHA -5
    # Bin  4 is for LHA -4
    # Bin  5 is for LHA -3
    # Bin  6 is for LHA -2
    # Bin  7 is for LHA -1
    # Bin  8 is for LHA  0
    # Bin  9 is for LHA  1
    # Bin 10 is for LHA  2
    # Bin 11 is for LHA  3
    # Bin 12 is for LHA  4
    # Bin 13 is for LHA  5
    # Bin 14 is for LHA  6
    
    # If the LHA is larger that 6 or smaller than -6 they are not
    # assigned a bin.
    
    def bin (self):
        if (self.dec.deg > 70):
            return 1
        else:
            localHrAngle = self.localHrAngle()
            
            # First make sure the object is in the range -6 .. 6
            
            if ((localHrAngle <= -6) and (localHrAngle <= 6)): # assign a bin
                return localHrAngle + 8
            else:
                return -1

# First determine which bin the two objects are in which is based on the LST.

    # define == operator
    def __eq__ (self,y):
        if ((self.ra == y.ra) and (self.dec == y.dec)):
            return 1
        else:
            return 0

    # define < operation for 
    def __lt__ (self,y):
        xBinNumber = self.bin()
        yBinNumber = y.bin()
        
        if (self.bin() == y.bin()): # use declination to sort
            return self.dec <= y.dec
        else: # bins are not equal use bin number to sort
            return self.bin() < y.bin()
        
    def __le__ (self,y):
        if (self == y):
            return 1
        else:
            return self < y

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

    observingPosition = EarthLocation(lat    = ( 34+49/60+32/3600) *u.deg,
                                      lon    =-(118+1 /60+27*3600) *u.deg,
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

    # Extract the hour, minute, and second from the mean LST.
    # Be nice if there were methods in the astropy package.
    
    lst_hr  = int(str(meanLST)[0:2])
    lst_min = int(str(meanLST)[3:5])
    lst_sec = int(str(meanLST)[6:8])
    
    print lst_hr, lst_min, lst_sec

    print '---------------------'  
    
    # Grab the Simbad data base
    
    from astroquery.simbad import Simbad

    # This query will get all of the Messier objects.
    
    table = Simbad.query_object ('M *', wildcard=True, verbose=False, get_query_payload=False)

    # There are 110 objects, len(table) get the length for the
    # range function.
        
    for i in range(len(table)):
        print table[i]['MAIN_ID']
        print table[i]['RA']
        print table[i]['DEC']
        ra = table[i]['RA']
        dec = table[i]['DEC']
        ra_hr   = ra[0:2]
        ra_min  = ra[3:5]
        ra_sec  = ra[6:8]
        dec_deg = dec[0:3]
        dec_min = dec[4:6]
        dec_sec = dec[7:12]
        if (dec_sec == ''):
            dec_sec = 0
        print 'i   : ', i
        print 'ra  : ', ra_hr,   ra_min,  ra_sec
        print 'dec : ', dec_deg, dec_min, dec_sec
        newObject = ObjectRaDec (Ra  (ra_hr, ra_min, ra_sec),
                                Dec (dec_deg, dec_min, dec_sec),
                                Lst (lst_hr, lst_min, lst_sec))
        if (i == 0):
            objectTable = [newObject]
        else:
            objectTable.append(newObject)
    
    if (objectTable[0] < objectTable[1]):
        print 'less than is true'
    else:
        print 'less than is false'
        
    objectTable.sort()
            
    print '---------------------'
    # When initializing the object I really only want to use one global LST
    # value, I'm not sure how to implement that in Python.
    
    object1 = ObjectRaDec(Ra(12,13,14),Dec(1,2,3), Lst(lst_hr, lst_min, lst_sec))
    object2 = ObjectRaDec(Ra(9,1,2),   Dec(3,4,5), Lst(lst_hr, lst_min, lst_sec))
    object3 = object2
    
    object1.write()
    object2.write()
    object3.write()
    
    print 'subtract ra          : ', object1.ra - object2.ra
    print 'object1.localHrAngle : ', object1.localHrAngle()
    print 'object2.localHrAngle : ', object2.localHrAngle()
    print 'object3.localHrAngle : ', object3.localHrAngle()
    print 'object1.bin          : ', object1.bin()
    print 'object1.ra.getSeconds() : ', object1.ra.getSeconds()
    
    print 'testing == operator'
    
    if (object3 == object2):
        print 'equal is True'
    else:
        print 'equal is False'

    if (object1 < object2):
        print 'less than true'
    else:
        print 'less than false'
