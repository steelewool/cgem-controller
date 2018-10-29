
import objectRaDec
from raDecLst import Ra, Dec, Lst, Alt, Azi
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
    
    def __init__(self):
        
        # Hard wired to Frazier Park. Need to add lat/lon/height as an
        # argument to the class.
        
        observingPosition = EarthLocation(
            lat    = ( 34.0 + 49.0/60.0 + 32.0/3600.0) * u.deg,
            lon    =-(118.0 +  1.0/60.0 + 27.0*3600.0) * u.deg,
            height = (5000 * 0.3048)                   * u.m)
        
        date = astropy.time.Time(astropy.time.Time.now(),
                                 scale='utc',
                                 location=observingPosition)
        
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
    
        # print lst_hr, lst_min, lst_sec
   
        # Grab the Simbad data base
    
        from astroquery.simbad import Simbad

        # This query will get all of the Messier objects. Note that the table
        # isn't modified - but instead I copy the data to the objectTable list
        # which does get sorted my observability.
    
        table = Simbad.query_object ('M *', wildcard=True, verbose=False)
        
        # This loop goes through the table of messier objects obtained from
        # the query above and moves the objects into the array objectTable.
        
        for i in range(len(table)):
            ra      = table[i]['RA']
            dec     = table[i]['DEC']
            
            # print 'ra from simbad query  : ', ra
            # print 'dec from simbad query : ', dec
            
            # These substring operations have me concernedNeed to debug
            # to make things are working correctly.
            
            # This works correctly because the objects from simbad query
            # come in a very fixed format.
            
            ra_hr   = ra[0:2]
            ra_min  = ra[3:5]
            ra_sec  = ra[6:8]
            if ra_sec == '':
                ra_sec = 0
            dec_deg = dec[0:3]
            dec_min = dec[4:6]
            dec_sec = dec[7:12]
            if dec_sec == '':
                dec_sec = 0
                
            # Need to calculate the altitude and azimuth for each of the
            # objects here.
            
            raHrMinSec   = ra_hr   + 'h' + ra_min  + 'm' + ra_sec  + 's'
            if dec_sec > 0:
                decDegMinSec = dec_deg + 'd' + dec_min + 'm' + dec_sec + 's'
            else:
                decDegMinSec = dec_deg + 'd' + dec_min + 'm' + '00' + 's'
            # print 'raHrMinSec   : ', raHrMinSec
            # print 'decDegMinSec : ', decDegMinSec
                          
            skyCoord = SkyCoord (raHrMinSec + ' ' + decDegMinSec, frame='icrs')

            altAzi = skyCoord.transform_to(AltAz(obstime=date,location=observingPosition))

            #print 'alt : ', altAzi.alt.degree
            #print 'azi : ', altAzi.az.degree
            
            newObject = objectRaDec.ObjectRaDec(table[i]['MAIN_ID'],
                                                Ra  (ra_hr,   ra_min,  ra_sec),
                                                Dec (dec_deg, dec_min, dec_sec),
                                                Lst (lst_hr,  lst_min, lst_sec),
                                                Alt (altAzi.alt.degree),
                                                Azi (altAzi.az.degree))
            
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

    print 'length: ', len(messierObjects.objectTable)
    
    for i in range (len(messierObjects.objectTable)):
        #print 'bin: ', messierObjects.objectTable[i].binNumber
        #if (messierObjects.objectTable[i].binNumber > 0):
        messierObjects.objectTable[i].write()
        # print 'ra hr: ', messierObjects.objectTable[i].ra.hr
            
