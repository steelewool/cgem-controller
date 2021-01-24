import serial
import convertRaDecToCgemUnits

# Another neat idea would be to have this script spawn the virtual
# serial port
# Since simulator only runs while we are simulating (duh) it could
# runs
# nullmodem.sh before attempting to establish the serial interface.

serialPort = './pty2'
ser = serial.Serial(port=serialPort,timeout=1)

class Simulator:

  def __init__ (self):
    print ('class Simulator __init__')
    self.raConversion  = convertRaDecToCgemUnits.Ra()
    self.decConversion = convertRaDecToCgemUnits.Dec()
    print ('exit __init__')

  def parse_command(self, prefix):
    print ('Start of parse_command, prefix: ', prefix)
    
    if prefix == 'r':
      commandText = ser.read(20)
      print ("Read command parameters: '{0}'".format(commandText))

      # Split up the two arguments which are separated by a ','.
      
      args = commandText.split(',', 2)
      
      # The two variables testscopeRa and telescopeDec will be used
      # to simulate the current position of the telescope
      
      self.telescopeRa = self.raConversion.fromCgem(args[0])
      
      self.telecopeRaCgem = (
          convertRaDecToCgemUnits.Ra(float(self.telescopeRa[0]),
                                     float(self.telescopeRa[1]),
                                     float(self.telescopeRa[2]))).toCgem()
                                     
      print ('self.telescopeRaCgem : ', self.telecopeRaCgem)
      
      # If the declination is outside of the range -90 to +90 then
      # it needs to be converted back. The telescopeDec variable
      # needs to be corrected before calling the toCgem method.
      
      self.telescopeDec = self.decConversion.fromCgem(args[1])
      
      self.telescopeDecGem = (convertRaDecToCgemUnits.Dec
                              (float(self.telescopeDec[0]),
                               float(self.telescopeDec[1]),
                               float(self.telescopeDec[2]))).toCgem()
      print ('ser.write #')
      ser.write("#")
    elif prefix == 'K':
        argument = ser.read(1)
        print (ser.write with argument: ', argument)
        ser.write (argument + '#')
    elif prefix == 'L':
        ser.write ('0#')
    elif prefix == 'e':
        outputCommand = self.telecopeRaCgem + ',' + self.telescopeDecGem + '#'
        ser.write (outputCommand)
    else:
        print ('Unknown command')

if __name__ == '__main__':
  print ('Start of Simulator')
  
  done = False
  sim = Simulator()

  print ('Enter while loop')
  
  while not done:
    if ser.isOpen() == False:
      done = True
    else:
      cmd = ser.read(1)
      print ('cmd: ', cmd)
      if cmd != '':
        sim.parse_command(cmd)
        if cmd == 'q':
          done = True

