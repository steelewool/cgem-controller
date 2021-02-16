# The class ObjectRaDec, which is not a very description name is
# intended to provide sorting of a list of objects for the 'best'
# observing order.

# Not sure where this from came from - uness LiClipse added it.

# from pyraf.iraffunctions import substr

# As of 9/25/18 I have the LST embedded in the ObjectRaDec object.
# It may make more sense to place in the list -
# but but is still a deferred design detail.

from raDecLst import Ra, Dec, Lst, Alt, Azi

class ObjectRaDec:
    def __init__ (self,
                  name = ' ',
                  catName = ' ',
                  tableRa = 0.0,
                  tableDec = 0.0,
                  ra  = Ra(),
                  dec = Dec(),
                  lst = Lst(),
                  alt = Alt(),
                  azi = Azi()):
        self.name      = name
        self.catName   = catName
        self.tableRa   = tableRa
        self.tableDec  = tableDec
        self.ra        = ra
        self.dec       = dec
        self.lst       = lst
        self.alt       = alt
        self.azi       = azi
        self.binNumber = self.bin()

    def updateLst(self,lst):
        self.lst = lst

    def updateAltAzi (self, alt, azi):
        self.alt = alt
        self.azi = azi
        
    def localHrAngle(self):
        localHourAngle =(self.ra.getSeconds() - self.lst.getSeconds())/(3600*15)
        if localHourAngle > 12:
            localHourAngle = localHourAngle - 24
        return int(localHourAngle)

    # This function will the bin value for searching and sorting.
    #
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
        # This code is looking for objects with alititdes less than
        # 20 degrees. Objects lower that than are not observable from
        # my location.
        if self.alt.deg < 20.0:
            return -1
        
        # Using 60. If I go to 70 degrees for bin 1 I
        # start losing objects.
        
        if (float(self.dec.deg) > 60.0):
            return 1
        else:
            localHrAngle = self.localHrAngle()
            # First make sure the object is in the range -6 .. 6
            if ((-6 <= localHrAngle) and (localHrAngle <= 6)): # assign a bin
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
        if (self.bin() == y.bin()): # use declination to sort
            # if bin is an odd number then use <= to sort
            # if bin is even use >= to sort
            #print ('self.dec.deg: ', self.dec.deg, 'y.dec: ', y.dec.deg)
            if ((self.bin() % 2) == 0):
                return self.dec.deg <= y.dec.deg
            else:
                return y.dec.deg <= self.dec.deg
        else: # bins are not equal use bin number to sort
            return self.bin() < y.bin()
        
    def __le__ (self,y):
        if (self == y):
            return 1
        else:
            return self < y
        
    def __gt__ (self,y):
        return not(self < y)
    
    def __ge__ (self,y):
        if (self.bin == y.bin()):
            return self.dec <= y.dec
        else:
            return not(self.bin < y.bin)

# If the objects declination is > 70 degrees north then it goes in bin 1.
# The other 12 bins start with the local angle of -90 degree going each by
# 15 degree increments until I get to +90 degree.

# Yet another questions, whey am I having to use getLst() instead of lst?
        
    def write(self):
        print ()
        print ('Bin number      : ' + str(self.bin()))
        print ('Name            : ' + str(self.name))
        print ('Catalog name    : ' + str(self.catName))
        print ('RA   hr min sec : ' + str(self.ra.hr)   + ':' + str(self.ra.min)  + ':' + str(self.ra.sec))
        print ('Dec deg min sec : ' + str(self.dec.deg) + ':' + str(self.dec.min) + ':' + str(self.ra.sec))
        print ('Local Hour Angle: ' + str(self.localHrAngle()))
        print ('LST  hr min sec : ' + str(self.lst.hr)  + ':' + str(self.lst.min) + ':' + str(self.lst.sec))
        print ('Altitude        : ' + str(int(self.alt.deg)))
        print ('Azimuth         : ' + str(int(self.azi.deg)))
        print ()

# Using the paradigm supplied by Zach to be able to test this class

if __name__ == '__main__':

    import astropy.time
    from   astropy.time        import Time
    from   astropy             import units as u
    from   astropy.coordinates import EarthLocation
    from   astropy.coordinates import SkyCoord
    from   astropy.coordinates import AltAz

    observingPosition = EarthLocation(lat    = ( 34+49/60+32/3600) *u.deg,
                                      lon    =-(118+1 /60+27*3600) *u.deg,
                                      height = (5000 * 0.3048)     *u.m)
    
    #print 'observingPosition            : ', observingPosition
    #print 'astropy.time.Time.now()      : ', astropy.time.Time.now()

    date = astropy.time.Time(astropy.time.Time.now(),
                             scale='utc',
                             location=observingPosition)
    
    #print 'date                         : ', date
    #print 'date.now()                   : ', date.now()
    #print 'date.sidereal_time(mean)     : ', date.sidereal_time('mean')
    #print 'date.sidereal_time(apparent) : ', date.sidereal_time('apparent')

# As pointed out in issue 62 the extraction of LST was not being done
# correctly here. This is also done in messierObjectList and perhaps
# other places.

    meanLST = date.sidereal_time('mean')
    #print 'meanLST                      : ', meanLST

    # Extract the hour, minute, and second from the mean LST.
    # Be nice if there were methods in the astropy package.
    
    positionH = str(meanLST).find('h')
    positionM = str(meanLST).find('m')
        
    # Extract the hour, minute, and second from the mean LST.
    # Be nice if there were methods in the astropy package.
    
    lst_hr  = int(str(meanLST)[0          :positionH])
    lst_min = int(str(meanLST)[positionH+1:positionM])
    lst_sec = int(str(meanLST)[positionM+1:positionM+3])
    
    # Grab the Simbad data base
    
    from astroquery.simbad import Simbad

    # This query will get all of the Messier objects. Note that the table
    # isn't modified - but instead I copy the data to the objectTable list
    # which does get sorted my observability.
    
    table = Simbad.query_object ('M *', wildcard=True, verbose=False, get_query_payload=False)

    # There are 110 objects, len(table) get the length for the
    # range function.
    
    for i in range(len(table)):
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
            
        raHrMinSec   = ra_hr   + 'h' + ra_min  + 'm' + ra_sec  + 's'
        if float(dec_sec) > 0:
            decDegMinSec = dec_deg + 'd' + dec_min + 'm' + dec_sec + 's'
        else:
            decDegMinSec = dec_deg + 'd' + dec_min + 'm' + '00' + 's'
                          
        skyCoord = SkyCoord (raHrMinSec + ' ' + decDegMinSec, frame='icrs')

        altAzi = skyCoord.transform_to(AltAz(obstime=date,location=observingPosition))

        newObject = ObjectRaDec (table[i]['MAIN_ID'],
                                 Ra  (ra_hr, ra_min, ra_sec),
                                 Dec (dec_deg, dec_min, dec_sec),
                                 Lst (lst_hr, lst_min, lst_sec),
                                 Alt (altAzi.alt.degree),
                                 Azi (altAzi.az.degree))
        if (i == 0):
            objectTable = [newObject]
        else:
            objectTable.append(newObject)

    #print 'Before sort.'
    
    objectTable[0].write()
    objectTable[len(objectTable)-1].write()

    objectTable.sort()
    
    # Remove any objects that have a negative bin number
    
    #print 'After sort.'

    for i in range(len(objectTable)):
        if (objectTable[i].binNumber > 0):
            #print 'Index     : ', i
            #print 'Bin number: ', objectTable[i].bin()
            #print 'Bin number: ', objectTable[i].binNumber
            #print 'LHA       : ', objectTable[i].localHrAngle()
            objectTable[i].write()

#    print 'Bin number: ', objectTable[len(objectTable)-1].bin()
#    print 'Bin number: ', objectTable[len(objectTable)-1].binNumber
#    print 'LHA       : ', objectTable[len(objectTable)-1].localHrAngle()
#    objectTable[len(objectTable)-1].write()
       
    #print '---------------------'
    # When initializing the object I really only want to use one global LST
    # value, I'm not sure how to implement that in Python.
    
    object1 = ObjectRaDec('object1', Ra(12,13,14),Dec(1,2,3), Lst(lst_hr, lst_min, lst_sec))
    object2 = ObjectRaDec(ra = Ra(9,1,2),  dec = Dec(3,4,5), lst = Lst(lst_hr, lst_min, lst_sec))
    object3 = object2
    
    object1.write()
    object2.write()
    object3.write()
    
    #print 'subtract ra          : ', object1.ra - object2.ra
    #print 'object1.localHrAngle : ', object1.localHrAngle()
    #print 'object2.localHrAngle : ', object2.localHrAngle()
    #print 'object3.localHrAngle : ', object3.localHrAngle()
    #print 'object1.bin          : ', object1.bin()
    #print 'object1.ra.getSeconds() : ', object1.ra.getSeconds()
    
    #print 'testing == operator'
    
    if (object3 == object2):
        print ('equal is True')
    else:
        print ('equal is False')

    if (object1 < object2):
        print ('less than true')
    else:
        print ('less than false')
