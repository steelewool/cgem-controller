# The class ObjectRaDec, which is not a very description name is
# intended to provide sorting of a list of objects for the 'best'
# observing order.

class Ra:
    def __init__ (self, hr = 0, min = 0, sec = 0):
        self.hr  = hr
        self.min = min
        self.sec = sec
    def getHr(self):
        return self.hr
    def getMin(self):
        return self.min
    def getSec(self):
        return self.sec
    def getSeconds(self):
        return ((self.hr * 60.0 * 60.0) + (self.min  * 60.0) + self.sec) * 15.0
    
class Dec():
    def __init__ (self, deg = 0, min = 0, sec = 0):
        self.deg = deg
        self.min = min
        self.sec = sec
    def getDeg(self):
        return self.deg
    def getMin(self):
        return self.min
    def getSec(self):
        return self.sec
    def getSeconds(self):
        return (self.deg * 60.0 * 60.0) + (self.min  * 60.0) + self.sec

class Lst:
    def __init__ (self, hr = 0, min = 0, sec = 0):
        self.hr  = hr
        self.min = min
        self.sec = sec
    def getHr(self):
        return self.hr
    def getMin(self):
        return self.min
    def getSec(self):
        return self.sec
    def getSeconds(self):
        return ((self.hr * 60.0 * 60.0) + (self.min * 60.0) + self.sec) * 15.0
    
class ObjectRaDec:
    def __init__ (self, ra=Ra(), dec=Dec(), lst=Lst()):
        self.ra  = ra
        self.dec = dec
        self.lst = lst
    def getRa(self):
        return self.ra
    def getDec(self):
        return self.dec
    def getLst(self):
        return self.lst
    def getSeconds(self):
        (self.deg * 60.0 * 60.0) + (self.min * 60.0) + self.sec
    
# First determine which bin the two objects are in which is based on the LST.

    def __eq__ (x,y):
        if ((x.ra == y.ra) and (x.dec == y.dec)):
            return 0
        else:
            return -1

    def __lt__ (x,y):
        xRaInSeconds  = x.getRa().getSeconds()
        yRaInSeconds  = y.getRa().getSeconds()
        xDecInSeconds = x.getDec().getSeconds()
        yDecInSeconds = y.getDec().getSeconds()

        if (x.getDec().getDeg() > 70):
            xBin = 1
        else:
            print 'need code to computer xBin'
        return 0

# Using the paradigm supplied by Zach to be able to test this class

if __name__ == '__main__':

    ra  = Ra(10,11,12)
    dec = Dec()

    print 'a ', ra.getHr()
    print 'b ', ra.getMin()
    print 'c ', ra.getSec()
    
    object1 = ObjectRaDec(Ra(12,13,14),Dec(1,2,3),Lst(4,5,6))
    object2 = ObjectRaDec(Ra(0,1,2),Dec(3,4,5),Lst(6,7,8))

# Not sure if the get's are necessary

    print 'x ', object1.getRa().getHr()
    print 'y ', object1.getDec().getDeg()
    print 'z ', object1.getLst().getHr()
    
    object1.ra.hr   = 10
#    object1.dec.deg =  0
#    object2.ra.hr   = 15
#    object2.dec.deg =  0

    print object1.ra.hr
    print object2.dec.deg

    if (object1 == object2):
        print 'equal is True'
    else:
        print 'equal to False'

    if (object1 < object2):
        print 'less than true'
    else:
        print 'less than false'
