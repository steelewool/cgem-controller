
import objectRaDec
from   objectRaDec import Ra, Dec, Lst
import astropy.time
from   astropy.time        import Time
from   astropy             import units as u
from   astropy.coordinates import EarthLocation
from   astropy.coordinates import SkyCoord
 
class MessierObjectList:
    
    # Initialzation logic to create the the sorted list
    # As of right now I'm setting the time internally
    
    def __init__(self):
        observingPosition = EarthLocation(lat    = ( 34+49/60+32/3600) *u.deg,
                                          lon    =-(118+1 /60+27*3600) *u.deg,
                                          height = (5000 * 0.3048)     *u.m)

        date = astropy.time.Time(astropy.time.Time.now(),
                                 scale='utc',
                                 location=observingPosition)
    
        meanLST = date.sidereal_time('mean')
        print 'meanLST                      : ', meanLST

        # Extract the hour, minute, and second from the mean LST.
        # Be nice if there were methods in the astropy package.
        
        # This is not very robust. It fails with different LST values.
    
        lst_hr  = int(str(meanLST)[0:1])
        lst_min = int(str(meanLST)[2:4])
        lst_sec = int(str(meanLST)[5:7])
    
        print lst_hr, lst_min, lst_sec
   
        # Grab the Simbad data base
    
        from astroquery.simbad import Simbad

        # This query will get all of the Messier objects. Note that the table
        # isn't modified - but instead I copy the data to the objectTable list
        # which does get sorted my observability.
    
        table = Simbad.query_object ('M *', wildcard=True, verbose=False, get_query_payload=False)
        
        for i in range(len(table)):
            ra      = table[i]['RA']
            dec     = table[i]['DEC']
            ra_hr   = ra[0:2]
            ra_min  = ra[3:5]
            ra_sec  = ra[6:8]
            dec_deg = dec[0:3]
            dec_min = dec[4:6]
            dec_sec = dec[7:12]
            if (dec_sec == ''):
                dec_sec = 0
            newObject = objectRaDec.ObjectRaDec(table[i]['MAIN_ID'],
                                                 Ra  (ra_hr,   ra_min,  ra_sec),
                                                 Dec (dec_deg, dec_min, dec_sec),
                                                 Lst (lst_hr,  lst_min, lst_sec))
            if (i == 0):
                self.objectTable = [newObject]
            else:
                self.objectTable.append(newObject)

        # Sort the objects into a best fit for observing
        
        self.objectTable.sort()

if __name__ == '__main__':
        
    print 'main program entered'
    messierObjects = MessierObjectList()
    print messierObjects.objectTable[0].name
    
    for i in range (len(messierObjects.objectTable)):
        if (messierObjects.objectTable[i].binNumber > 0):
            messierObjects.objectTable[i].write()
            # print 'ra hr: ', messierObjects.objectTable[i].ra.hr
            