
class Ra:
    def __init__ (self, hr = 0, min = 0, sec = 0.0):
        self.hr  = hr
        self.min = min
        self.sec = sec

    def getSeconds(self):
        return ((float(self.hr )   * 3600.0) +
                (float(self.min)   *   60.0) +
                (float(self.sec)))           * 15.0
    # define subtracttion
    def __sub__ (self, y):
        xSeconds = self.getSeconds()
        ySeconds = y.getSeconds()
        return xSeconds - ySeconds
    
class Dec():
    def __init__ (self, deg = 0, min = 0, sec = 0.0):
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
    def __init__ (self, hr = 0, min = 0, sec = 0.0):
        self.hr  = hr
        self.min = min
        self.sec = sec
    def getSeconds(self):
        return ((self.hr * 60.0 * 60.0) + (self.min * 60.0) + self.sec) * 15.0

    # define subtracttion
    def __sub__ (self, y):
        xSeconds = self.getSeconds()
        ySeconds = y.getSeconds()
        return xSeconds - ySeconds

class Alt:
    def __init__ (self, deg = 0.0):
        self.deg = deg
    def getSeconds(self):
        return (float(self.deg) * 60.0 * 60.0)
    
class Azi:
    def __init__ (self, deg = 0.0):
        self.deg = deg
    def getSeconds(self):
        return (float(self.deg) * 60.0 * 60.0)
    
