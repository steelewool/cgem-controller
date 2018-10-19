
import objectRaDec
from   objectRaDec import Ra, Dec, Lst
import astropy.time
from   astropy.time        import Time
from   astropy             import units as u
from   astropy.coordinates import EarthLocation
from   astropy.coordinates import SkyCoord
from datetime import date

 
class MessierObjectList:
    
    # Initialzation logic to create the the sorted list
    # As of right now I'm setting the time internally
    
    def __init__(self):
        
        # Hard wired to Frazier Park. Need to add lat/lon/height as an
        # argument to the class.
        
        observingPosition = EarthLocation(
            lat    = ( 34.0 + 49.0/60.0 + 32.0/3600.0) * u.deg,
            lon    =-(118.0 +  1.0/60.0 + 27.0*3600.0) * u.deg,
            height = (5000 * 0.3048)                   *   u.m)
        
        date = astropy.time.Time(astropy.time.Time.now(),
                                 scale='utc',
                                 location=observingPosition)
        
        print 'date : ', date
        
        # Commented out for now, but this is the logic from predict_transit
        # for getting alt/azi of an object:

        # aa = AltAz(location=observingPosition, obstime=observingNextTransitTime)

        # ra = root.findtext('rightascension')
        # dec = root.findtext('declination')
                            
        # raHrMinSec = ra[0:2] + 'h' + ra[3:5] + 'm' + ra[6:8] + 's'
        # decDegMinSec = dec[0:3] + 'd' + dec[4:6] + 'm' + dec[8:10] + 's'
                            
        # skyCoord = SkyCoord (raHrMinSec + ' ' + decDegMinSec, frame='icrs')

        # altAzi = skyCoord.transform_to(AltAz(obstime=observingNextTransitTime,location=observingPosition))

        # print altAzi.alt.degree
        

        meanLST = date.sidereal_time('mean')
        print 'meanLST : ', meanLST

        # Use the 'h' and 'm' to extract the hour, minute, and second
        # from the meanLST
        
        positionH = str(meanLST).find('h')
        positionM = str(meanLST).find('m')
        
        # Extract the hour, minute, and second from the mean LST.
        # Be nice if there were methods in the astropy package.
    
        lst_hr  = int(str(meanLST)[0          :positionH])
        lst_min = int(str(meanLST)[positionH+1:positionM])
        lst_sec = int(str(meanLST)[positionM+1:positionM+3])
    
        print lst_hr, lst_min, lst_sec
   
        # Grab the Simbad data base
    
        from astroquery.simbad import Simbad

        # This query will get all of the Messier objects. Note that the table
        # isn't modified - but instead I copy the data to the objectTable list
        # which does get sorted my observability.
    
        table = Simbad.query_object ('M *', wildcard=True, verbose=False)
        # does not work on the pi: , get_query_payload=False)
        
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
            
