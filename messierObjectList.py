
import objectRaDec
from   raDecLst import Ra, Dec, Lst, Alt, Azi
import astropy.time
from   astropy.time        import Time
from   astropy             import units as u
from   astropy.coordinates import EarthLocation
from   astropy.coordinates import SkyCoord
from   astropy.coordinates import AltAz
from   datetime import date

class MessierObjectList:
    
    # Initialzation logic to create the the sorted list

    # As of right now I'm setting the time internally

    def setLocalTime(self):

        # Hard wired to Frazier Park. Need to add lat/lon/height as an
        # argument to the class.

        # Set the latitude, longitude, and elevation of the
        # position of the observer.

        self.observingPosition = EarthLocation(                 \
            lat    = ( 34.0 + 49.0/60.0 + 32.0/3600.0) * u.deg, \
            lon    =-(118.0 +  1.0/60.0 + 27.0*3600.0) * u.deg, \
            height = (5000 * 0.3048)                   * u.m)

        # Get the current time
        
        self.dateTime = astropy.time.Time(astropy.time.Time.now(), \
                                 scale='utc',                      \
                                 location=self.observingPosition)

        self.meanLST = self.dateTime.sidereal_time('mean')

        #print ('meanLST : ', self.meanLST)

        # Use the 'h' and 'm' to extract the hour, minute, and second
        # from the meanLST
        
        self.positionH = str(self.meanLST).find('h')
        self.positionM = str(self.meanLST).find('m')
        
        # Extract the hour, minute, and second from the mean LST.
        # Be nice if there were methods in the astropy package.
    
        self.lst_hr  = int(str(self.meanLST)[0          :self.positionH])
        self.lst_min = int(str(self.meanLST)[self.positionH+1:self.positionM])
        self.lst_sec = int(str(self.meanLST)[self.positionM+1:self.positionM+3])

    def __init__(self):

        self.setLocalTime()
        
        # Grab the Simbad data base
        # Getting the following warning, which I'm not sure how to fix.

# WARNING: AstropyDeprecationWarning: astropy.extern.six will be removed
# in 4.0, use the six module directly if it is still needed
# [astropy.extern.six]

        from astroquery.simbad import Simbad

        # This query will get all of the Messier objects. Note that the table
        # isn't modified - but instead I copy the data to the objectTable
        # list which does get sorted my observability.

        # All of the table* statements below worked without any
        # errors when I was running Python3 in a terminal mode.

        Simbad.ROW_LIMIT = 120
        try:
            tableMessier   = Simbad.query_criteria(cat='M')
            tableMessierOk = True
            print ('Length of Messier table : ', len(tableMessier))
        except:
            tableMessierOk = False
            print ('tableMessier failed.')
        
        Simbad.ROW_LIMIT = 5000
        try:
            tableMGC     = Simbad.query_criteria('Vmag<12.0', \
                                                 cat='MGC')
            tableMgcOk   = True
            print ('Length of MGC table : ', len(tableMGC))
        except:
            tableMgcOk   = False
            print ('tableMCG failed')

        try:
            tableIC      = Simbad.query_criteria('Vmag<12.0', \
                                                 cat='IC')
            tableIcOk    = True
            print ('Length of IC table : ', len(tableIC))
        except:
            tableIcOk    = False
            print ('tableIC failed')

        try:
            tableHIP     = Simbad.query_criteria('Vmag<12.0', \
                                                 cat='HIP')
            tableHipOk   = True
            print ('Length of HIP table : ', len(tableHIP))
        except:
            tableHipOk   = False
            print ('tableHIP failed')
            
        Simbad.ROW_LIMIT = 1000
        try:
            # With a row limit of 5000 things crash with the NGC catalog
            tableNGC         = Simbad.query_criteria('Vmag<12.0', \
                                                     cat='NGC')
            tableNgcOk = True
            print ('Length of NGC table : ', len(tableNGC))
        except:
            tableNgcOk = False
            print ('First attempt to access NGC table failed.')

        if tableNgcOk == False:
            Simbad.ROW_LIMIT /= 2
            try:
                # With a row limit of 5000 things crash with the NGC catalog
                tableNGC         = Simbad.query_criteria('Vmag<12.0', \
                                                         cat='NGC')
                tableNgcOk = True
                print ('Length of NGC table : ', len(tableNGC))
            except:
                tableNgcOk = False
                print ('Second attempt to access NGC table failed.')
                

        Simbad.ROW_LIMIT = 10000
        try:
            tableAll = Simbad.query_criteria('Vmag<12.0')
            tableAllOk = True
            print ('Length of All table : ', len(tableAll))
        except:
            tableAllOk = False
            print ('Attempt to access all catalogs failed.')

        # If the first attempt failed then cut the row limit in
        # half and try again.
        
        if tableAllOk == False:
            Simbad.ROW_LIMIT /= 2
            try:
                tableAll = Simbad.query_criteria('Vmag<12.0')
                tableAllOk = True
                print ('Length of All table : ', len(tableAll))
            except:
                tableAllOk = False
                print ('Second attempt to access all catalogs failed.')

        Simbad.ROW_LIMIT = 10000
        try:
            # With a limit of 10000 returned 5212 elements
            tablePL   = Simbad.query_criteria(otype='PL')
            tablePlOk = True
            print ('Length of table PL : ', len(tablePL))
        except:
            tablePlOk = False
            print ('tablePL is failing')


        # Need to merge the tables and eliminate duplicate items.
        # Or those with distances less than a few arc minutes.

        if tableMessierOk:
            table = tableMessier
        else:
            table = Simbad.query_object ('M *', wildcard=True, verbose=False)
            
        print ('Length of Messier objects table: ', len(table))
        
        # This loop goes through the table of messier objects obtained from
        # the query above and moves the objects into the array objectTable.
        
        for i in range(len(table)):
            self.tableRa  = table[i]['RA']
            self.tableDec = table[i]['DEC']
            self.extractRaDec (self.tableRa, self.tableDec)
            
            skyCoord = SkyCoord (self.raHrMinSec + ' ' + \
                                 self.decDegMinSec,      \
                                 frame='icrs')

            self.altAzi = skyCoord.transform_to(       \
                AltAz(obstime=self.dateTime,           \
                      location=self.observingPosition))

            newObject = objectRaDec.ObjectRaDec(                \
                table[i]['MAIN_ID'],                            \
                self.tableRa,                                   \
                self.tableDec,                                  \
                Ra  (self.ra_hr, self.ra_min, self.ra_sec),     \
                Dec (self.dec_deg, self.dec_min, self.dec_sec), \
                Lst (self.lst_hr,                               \
                     self.lst_min,                              \
                     self.lst_sec),                             \
                Alt (self.altAzi.alt.degree),                   \
                Azi (self.altAzi.az.degree))

            if (i == 0):
                self.objectTable = [newObject]
            else:
                self.objectTable.append(newObject)

        # Sort the objects into a best fit for observing
        # Invokes the function on line 141 which simply invokes the
        # function objectTable.sort.
        
        self.sort()
        
    def extractRaDec (self, ra, dec):
        # 2021 01 29 print ('ra from simbad query  : ', ra)
        # 2021 01 29 print ('dec from simbad query : ', dec)
            
        # These substring operations have me concernedNeed to debug
        # to make things are working correctly.
            
        # This works correctly because the objects from simbad query
        # come in a very fixed format.
            
        self.ra_hr   = ra[0:2]
        self.ra_min  = ra[3:5]
        self.ra_sec  = ra[6:8]
        if self.ra_sec == '':
            self.ra_sec = 0
        self.dec_deg = dec[0:3]
        self.dec_min = dec[4:6]
        self.dec_sec = dec[7:12]
        if self.dec_sec == '':
            self.dec_sec = 0
                
        # Need to calculate the altitude and azimuth for each of the
        # objects here.
            
        self.raHrMinSec   = self.ra_hr   + 'h' + \
                            self.ra_min  + 'm' + \
                            self.ra_sec  + 's'
        if float(self.dec_sec) > 0:
            self.decDegMinSec = self.dec_deg + 'd' + \
                                self.dec_min + 'm' + \
                                self.dec_sec + 's'
        else:
            self.decDegMinSec = self.dec_deg + 'd' + \
                                self.dec_min + 'm' + \
                                '00' + 's'

    # Sorting is based upon local hour angle and the RA and Declination of
    # the object. Before sorting the LST, altitude, azimuth of the objects MUST
    # be updated. The objectTable is defined in the file objectRaDec.py
    
    def sort(self):
        self.objectTable.sort()

    def updateLstOfObjectTable(self):
        for i in range(len(self.objectTable)):
            self.setLocalTime()
            self.objectTable[i].updateLst(
                Lst(self.lst_hr,  \
                    self.lst_min, \
                    self.lst_sec))

    def updateAltAziOfObjectTable(self):
        for i in range(len(self.objectTable)):
            self.extractRaDec(self.objectTable[i].tableRa, \
                              self.objectTable[i].tableDec )
            
            skyCoord = SkyCoord (self.raHrMinSec + ' ' + self.decDegMinSec,
                                 frame='icrs')

            self.altAzi = skyCoord.transform_to(       \
                AltAz(obstime=self.dateTime,           \
                      location=self.observingPosition))
            self.objectTable[i].updateAltAzi(self.altAzi.alt, \
                                             self.altAzi.az);

    def updateObjectTable (self):
        self.updateLstOfObjectTable()
        self.updateAltAziOfObjectTable()
        self.sort()
        
if __name__ == '__main__':

    messierObjects = MessierObjectList()

    print (messierObjects.objectTable[0].name)

    print ('length: ', len(messierObjects.objectTable))

    # write() function is defined in objectRaDec.py line 123.
    # As of right now all of the print statements in the function
    # have been commented out.
    
#    for i in range (len(messierObjects.objectTable)):
#        messierObjects.objectTable[i].write()

    messierObjects.updateLstOfObjectTable()
    messierObjects.updateAltAziOfObjectTable()
    messierObjects.sort()

    messierObjects.updateObjectTable()

    objectNumber = 0
    for i in range (len(messierObjects.objectTable)):
        if messierObjects.objectTable[i].binNumber > 0:
            objectNumber = objectNumber+1
            print ('object Number : ', objectNumber)
            messierObjects.objectTable[i].write()
