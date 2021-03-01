
import objectRaDec
from   raDecLst import Ra, Dec, Lst, Alt, Azi
import astropy.time
from   astropy.time        import Time
from   astropy             import units as u
from   astropy.coordinates import EarthLocation
from   astropy.coordinates import SkyCoord
from   astropy.coordinates import AltAz
from   datetime import date

class SimbadObjectLists:
    
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

        # Use the 'h' and 'm' to extract the hour, minute, and second
        # from the meanLST
        
        self.positionH = str(self.meanLST).find('h')
        self.positionM = str(self.meanLST).find('m')
        
        # Extract the hour, minute, and second from the mean LST.
        # Be nice if there were methods in the astropy package.
    
        self.lst_hr  = int(str(self.meanLST)[0          :self.positionH])
        self.lst_min = int(str(self.meanLST)[self.positionH+1:self.positionM])
        self.lst_sec = int(str(self.meanLST)[self.positionM+1:self.positionM+3])

    def addToEndOfTable (self, flag, tableNew, catalogName):
        if flag:
            for i in range(len(tableNew)):
                if ((catalogName == 'G')   & (tableNew[i]['MAIN_ID'] == 'M  81'))        | \
                   ((catalogName == 'G')   & (tableNew[i]['MAIN_ID'] == 'M  82'))        | \
                   ((catalogName == 'ALL') & (tableNew[i]['MAIN_ID'] == 'NGC  7686'))    | \
                   ((catalogName == 'NGC') & (tableNew[i]['MAIN_ID'] == 'NGC  2169'))    | \
                   ((catalogName == 'NGC') & (tableNew[i]['MAIN_ID'] == 'NGC  1980'))    | \
                   ((catalogName == 'NGC') & (tableNew[i]['MAIN_ID'] == 'NGC  1981'))    | \
                   ((catalogName == 'NGC') & (tableNew[i]['MAIN_ID'] == 'NGC  2281'))    | \
                   ((catalogName == 'NGC') & (tableNew[i]['MAIN_ID'] == 'NGC  7686'))    | \
                   ((catalogName == 'NGC') & (tableNew[i]['MAIN_ID'] == 'NGC  7092'))    | \
                   ((catalogName == 'NGC') & (tableNew[i]['MAIN_ID'] == 'M  31'))        | \
                   ((catalogName == 'NGC') & (tableNew[i]['MAIN_ID'] == 'M  32'))        | \
                   ((catalogName == 'NGC') & (tableNew[i]['MAIN_ID'] == 'M  33'))        | \
                   ((catalogName == 'NGC') & (tableNew[i]['MAIN_ID'] == 'M  37'))        | \
                   ((catalogName == 'NGC') & (tableNew[i]['MAIN_ID'] == 'M  41'))        | \
                   ((catalogName == 'IC')  & (tableNew[i]['MAIN_ID'] == 'IC 2391   80')) | \
                   ((catalogName == 'OPC') & (tableNew[i]['MAIN_ID'] == 'M  36'))        | \
                   ((catalogName == 'OPC') & (tableNew[i]['MAIN_ID'] == 'M  37'))        | \
                   ((catalogName == 'OPC') & (tableNew[i]['MAIN_ID'] == 'M  38'))        | \
                   ((catalogName == 'OPC') & (tableNew[i]['MAIN_ID'] == 'M  41'))        | \
                   ((catalogName == 'G')   & (tableNew[i]['MAIN_ID'] == 'M  31'))        | \
                   ((catalogName == 'G')   & (tableNew[i]['MAIN_ID'] == 'M  32'))        | \
                   ((catalogName == 'G')   & (tableNew[i]['MAIN_ID'] == 'M  33'))        | \
                   ((catalogName == 'G')   & (tableNew[i]['MAIN_ID'] == 'M  51'))        | \
                   ((catalogName == 'G')   & (tableNew[i]['MAIN_ID'] == 'M  63'))        | \
                   ((catalogName == 'G')   & (tableNew[i]['MAIN_ID'] == 'M  77'))        | \
                   ((catalogName == 'G')   & (tableNew[i]['MAIN_ID'] == 'M  81'))        | \
                   ((catalogName == 'G')   & (tableNew[i]['MAIN_ID'] == 'M  82'))        | \
                   ((catalogName == 'G')   & (tableNew[i]['MAIN_ID'] == 'M  94'))        | \
                   ((catalogName == 'G')   & (tableNew[i]['MAIN_ID'] == 'M 101'))        | \
                   ((catalogName == 'G')   & (tableNew[i]['MAIN_ID'] == 'M 106'))        | \
                   ((catalogName == 'G')   & (tableNew[i]['MAIN_ID'] == 'M 110'))        | \
                   ((catalogName == 'G')   & (tableNew[i]['MAIN_ID'] == 'AM 0311-513')):
                    pass
                else:
                    self.tableRa  = tableNew[i]['RA']
                    self.tableDec = tableNew[i]['DEC']

                    try:
                        self.extractRaDec (self.tableRa, self.tableDec)
                        itemOk = True
                    except:
                        print ('in addToEndOfTable extractRaDec failed with i : ', i)
                        print ('name                                          : ',
                               tableNew[i]['MAIN_ID'])
                        print ('catalogName                                   : ',
                               catalogName)
                        itemOk = False

                    if itemOk:
                        skyCoord = SkyCoord (self.raHrMinSec + ' ' + \
                                             self.decDegMinSec,      \
                                             frame='icrs')
                
                        self.altAzi = skyCoord.transform_to(\
                                                            AltAz(obstime=self.dateTime,
                                                                  location=self.observingPosition))

                        newObject = objectRaDec.ObjectRaDec(\
                                                            tableNew[i]['MAIN_ID'],
                                                            catalogName,
                                                            self.tableRa,
                                                            self.tableDec,
                                                            Ra  (self.ra_hr, self.ra_min, self.ra_sec),
                                                            Dec (self.dec_deg, self.dec_min, self.dec_sec),
                                                            Lst (self.lst_hr,
                                                                 self.lst_min,
                                                                 self.lst_sec),
                                                            Alt (self.altAzi.alt.degree),
                                                            Azi (self.altAzi.az.degree))

                        self.objectTable.append(newObject)
    
    def __init__(self):
        self.setLocalTime()
        
        # Grab the Simbad data base
        # Getting the following warning, which I'm not sure how to fix.

# WARNING: AstropyDeprecationWarning: astropy.extern.six will be removed
# in 4.0, use the six module directly if it is still needed
# [astropy.extern.six]

        from astroquery.simbad import Simbad
        import time
        
        # This query will get all of the Messier objects. Note that the table
        # isn't modified - but instead I copy the data to the objectTable
        # list which does get sorted my observability.

        # All of the table* statements below worked without any
        # errors when I was running Python3 in a terminal mode.

        Simbad.ROW_LIMIT = 120
        try:
            time.sleep(2)
            tableMessier   = Simbad.query_criteria(cat='M')
            tableMessierOk = True
            print ('Length of Messier table : ', len(tableMessier))
        except:
            tableMessierOk = False
            print ('tableMessier failed.')
        
        Simbad.ROW_LIMIT = 100
        try:
            time.sleep(2)
            tableMgc     = Simbad.query_criteria('Vmag<10.5', \
                                                 cat='MGC')
            tableMgcOk   = True
            print ('Length of MGC table     : ', len(tableMgc))
        except:
            tableMgcOk   = False
            print ('tableMcg failed')


        Simbad.ROW_LIMIT = 200
        try:
            time.sleep(2)
            tableIc     = Simbad.query_criteria('Vmag<9.0', \
                                                 cat='ic')
            tableIcOk   = True
            print ('Length of IC table      : ', len(tableIc))
        except:
            tableIcOk   = False
            print ('tableIC failed')
            
        Simbad.ROW_LIMIT = 200
        try:
            # With a row limit of 5000 things crash with the NGC catalog
            time.sleep(2)
            tableNgc         = Simbad.query_criteria('Vmag<6.0', \
                                                     cat='NGC')
            tableNgcOk = True
            print ('Length of NGC table     : ', len(tableNgc))
        except:
            tableNgcOk = False
            print ('First attempt to access NGC table failed.')

        if tableNgcOk == False:
            Simbad.ROW_LIMIT /= 2
            try:
                # With a row limit of 5000 things crash with the NGC catalog
                time.sleep(2)
                tableNgc         = Simbad.query_criteria('Vmag<5.0', \
                                                         cat='NGC')
                tableNgcOk = True
                print ('Length of NGC table : ', len(tableNgc))
            except:
                tableNgcOk = False
                print ('Second attempt to access NGC table failed.')
                
        Simbad.ROW_LIMIT = 100
        try:
            time.sleep(2)
            tableAll = Simbad.query_criteria('Vmag<6.0')
            tableAllOk = True
            print ('Length of All table     : ', len(tableAll))
        except:
            tableAllOk = False
            print ('Attempt to access all catalogs failed.')

        # If the first attempt failed then cut the row limit in
        # half and try again.
        
        if tableAllOk == False:
            Simbad.ROW_LIMIT /= 2
            try:
                time.sleep(2)
                tableAll = Simbad.query_criteria('Vmag<5.0')
                tableAllOk = True
                print ('Length of All table     : ', len(tableAll))
            except:
                tableAllOk = False
                print ('Second attempt to access all catalogs failed.')

        # Looking for Planetary Nebulas
        Simbad.ROW_LIMIT = 100
        try:
            # With a limit of 10000 returned 5212 elements
            time.sleep(2)
            tablePl   = Simbad.query_criteria(otype='PL')
            tablePlOk = True
            print ('Length of table PL      : ', len(tablePl))
        except:
            tablePlOk = False
            print ('tablePL is failing')

        # Looking for Galaxies
        Simbad.ROW_LIMIT = 100
        try:
            # With a limit of 10000 returned 5212 elements
            time.sleep(2)
            tableG   = Simbad.query_criteria('Vmag<9.0', otype='G')
            tableGOk = True
            print ('Length of table G       : ', len(tableG))
        except:
            tableGOk = False
            print ('tableG is failing')

        # Looking for Globular Clusters
        Simbad.ROW_LIMIT = 100
        try:
            time.sleep(2)
            tableGlb   = Simbad.query_criteria(otype='glb')
            tableGlbOk = True
            print ('Length of table Glb     : ', len(tableGlb))
        except:
            tableGlbOk = False
            print ('tableGlb is failing')

        # Looking for Open Cluster
        Simbad.ROW_LIMIT = 100
        try:
            time.sleep(2)
            tableOpc   = Simbad.query_criteria('Vmag<6.5', otype='opc')
            tableOpcOk = True
            print ('Length of table Opc     : ', len(tableOpc))
        except:
            tableOpcOk = False
            print ('tableOpc is failing')

        # Need to merge the tables and eliminate duplicate items.
        # Or those with distances less than a few arc minutes.

        # When merging use the following priority order for which names are
        # kept:
        # Messier
        # NGC
        # PL
        # G
        # Glb
        # OpC
        # IC
        # MGC
        # All table, which in the end may not be useful
        
        if tableMessierOk:
            table = tableMessier
        else:
            time.sleep(2)
            table = Simbad.query_object ('M *', wildcard=True, verbose=False)
            
        # This loop goes through the table of messier objects obtained from
        # the query above and moves the objects into the array objectTable.
        
        for i in range(len(table)):
            self.tableRa  = table[i]['RA']
            self.tableDec = table[i]['DEC']

            try:
                self.extractRaDec (self.tableRa, self.tableDec)
            except:
                print ('in __init__ extracRaDec failed, i: ', i)
                print ('name                             : ', table[i]['MAIN_ID'])
                
            skyCoord = SkyCoord (self.raHrMinSec + ' ' + \
                                 self.decDegMinSec,      \
                                 frame='icrs')

            self.altAzi = skyCoord.transform_to(       \
                AltAz(obstime=self.dateTime,           \
                      location=self.observingPosition))

            newObject = objectRaDec.ObjectRaDec(                \
                table[i]['MAIN_ID'],                            \
                'Messier',                                      \
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

        # Add to the end of the object table the NGC objects

        self.addToEndOfTable (tableNgcOk, tableNgc, 'NGC')
        self.addToEndOfTable (tableMgcOk, tableMgc, 'MGC')
        self.addToEndOfTable (tableIcOk,  tableIc,  'IC')
        self.addToEndOfTable (tableAllOk, tableAll, 'ALL')
        self.addToEndOfTable (tablePlOk,  tablePl,  'PL')
        self.addToEndOfTable (tableGOk,   tableG,   'G')
        self.addToEndOfTable (tableGlbOk, tableGlb, 'GLB')
        self.addToEndOfTable (tableOpcOk, tableOpc, 'OPC')

        # Sort the objects into a best fit for observing
        # Invokes the function on line 141 which simply invokes the
        # function objectTable.sort.
        
        self.sort()
        
    def extractRaDec (self, ra, dec):
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

        # This was failing for the IC table (tableIC) objects. Their
        # format may be different,

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
        self.setLocalTime()
        for i in range(len(self.objectTable)):
            self.objectTable[i].updateLst(
                Lst(self.lst_hr,  \
                    self.lst_min, \
                    self.lst_sec))

    def updateAltAziOfObjectTable(self):
        for i in range(len(self.objectTable)):
            try:
                self.extractRaDec(self.objectTable[i].tableRa, \
                                  self.objectTable[i].tableDec )
            except:
                print ('in updateAltAziOfObjectTable extractRaDec failed on item, i : ', i)
                print ('object name                                                 : ',
                       self.objectTable[i].name)
                print ('catalog name                                                : ',
                       self.objectTable[i].catName)
                
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

    simbadObjects = SimbadObjectLists()

    print (simbadObjects.objectTable[0].name)

    print ('length: ', len(simbadObjects.objectTable))

    # write() function is defined in objectRaDec.py line 123.
    # As of right now all of the print statements in the function
    # have been commented out.
    
#    for i in range (len(simbadObjects.objectTable)):
#        simbadObjects.objectTable[i].write()

    simbadObjects.updateLstOfObjectTable()
    simbadObjects.updateAltAziOfObjectTable()
    simbadObjects.sort()

    simbadObjects.updateObjectTable()

    objectNumber = 0
    for i in range (len(simbadObjects.objectTable)):
        if simbadObjects.objectTable[i].binNumber > 0:
            objectNumber = objectNumber+1
            print ('object Number : ', objectNumber)
            simbadObjects.objectTable[i].write()
