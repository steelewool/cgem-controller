# The class ObjectRaDec, which is not a very description name is
# intended to provide sorting of a list of objects for the 'best'
# observing order.

class Ra():
    hr  = 0
    min = 0
    sec = 0

class Dec():
    deg = 0
    min = 0
    sec = 0
    
class ObjectRaDec():
    ra  = Ra()
    dec = Dec()

#   lst = Ra(15,10,0)
    lst = Ra()
    lst.hr  = 15
    lst.min = 10
    lst.sec = 0

# First determine which bin the two objects are in which is based on the LST.

    def __eq__ (x,y):
        if ((x.ra == y.ra) and (x.dec == y.dec)):
            return 0
        else:
            return -1;

    def __lt__ (x,y):

        xRaInSeconds  = ((x.ra.hr   * 60.0 * 60.0) + (x.ra.min  * 60.0) + x.ra.sec) * 15.0
        yRaInSeconds  = ((y.ra.hr   * 60.0 * 60.0) + (y.ra.min  * 60.0) + y.ra.sec) * 15.0
        xDecInSeconds =  (x.dec.deg * 60.0 * 60.0) + (x.dec.min * 60.0) + x.dec.sec
        yDecInSeconds =  (y.dec.deg * 60.0 * 60.0) + (y.dec.min * 60.0) + y.dec.sec

        if (x.dec.deg > 70):
            xBin = 1
        else:
            print 'need code to computer xBin'
            
        return 0

# Using the paradigm supplied by Zach to be able to test this class

if __name__ == '__main__':
    ra  = Ra()
    dec = Dec()

    object1 = ObjectRaDec()
    object2 = ObjectRaDec()

    object1.ra.hr   = 10
    object1.dec.deg =  0
    object2.ra.hr   = 15
    object2.dec.deg =  0

    if (object1 == object2):
        print 'equal is True'
    else:
        print 'equal to False'

    if (object1 < object2):
        print 'less than true'
    else:
        print 'less than false'
