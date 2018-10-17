import serial
import convertRaDecToCgemUnits

# Another neat idea would be to have this script spawn the virtual serial port
# Since simulator only runs while we are simulating (duh) it could runs
# nullmodem.sh before attempting to establish the serial interface.

ser = serial.Serial(
    port = './pty2',
    timeout=1)

class TelescopeSim:
  
  # Not sure if I have to declare these here, but it doesn't hurt to do so.
  
  raConversion  = convertRaDecToCgemUnits.Ra()
  decConversion = convertRaDecToCgemUnits.Dec()

  def parse_command(self, prefix):
    if prefix == 'r':
      commandText = ser.read(20)
#      print "Read command parameters: '{0}'".format(commandText)

      # Split up the two arguments which are separated by a ','.
      
      args = commandText.split(',', 2)
      
      # The two variables testscopeRa and telescopeDec will be used
      # to simulate the current position of the telescope
      
      self.telescopeRa = self.raConversion.fromCgem(args[0])
      
      self.telecopeRaCgem = (
          convertRaDecToCgemUnits.Ra(float(self.telescopeRa[0]),
                                     float(self.telescopeRa[1]),
                                     float(self.telescopeRa[2]))).toCgem()
                                     
#      print 'self.telescopeRaCgem : ', self.telecopeRaCgem
      
      # If the declination is outside of the range -90 to +90 then
      # it needs to be converted back. The telescopeDec variable
      # needs to be corrected before calling the toCgem method.
      
      self.telescopeDec = self.decConversion.fromCgem(args[1])
      
      self.telescopeDecGem = (convertRaDecToCgemUnits.Dec
                              (float(self.telescopeDec[0]),
                               float(self.telescopeDec[1]),
                               float(self.telescopeDec[2]))).toCgem()
      ser.write("#")
    elif prefix == 'K':
        argument = ser.read(1)
        ser.write (argument + '#')
    elif prefix == 'L':
        ser.write ('0#')
    elif prefix == 'e':
        # TODO: Store values from GOTO command (r/R) and return that here
        
        outputCommand = self.telecopeRaCgem+','+self.telescopeDecGem+'#'
#        print 'outputCommand : ', outputCommand
        ser.write (outputCommand)
                                              

#        print 'telescopeRaCgem : ', a.toCgem(), x.toCgem()
        
    else:
        print "Unknown command"

if __name__ == '__main__':
  done = False
  sim = TelescopeSim()
  
  while not done:
    cmd = ser.read(1)
    if cmd != '':
#      print "Read command-char '{0}'".format(cmd)
      sim.parse_command(cmd)
    if cmd == 'q':
      print "Ready to quit"
      done = True

