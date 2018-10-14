import serial
import convertRaDecToCgemUnits

# Another neat idea would be to have this script spawn the virtual serial port
ser = serial.Serial(
    port = './pty2',
    timeout=1)

class TelescopeSim:
  
  raConversion  = convertRaDecToCgemUnits.Ra()
  decConversion = convertRaDecToCgemUnits.Dec()
  
  def parse_command(self, prefix):
    if prefix == 'r':
      commandText = ser.read(20)
      print "Read command parameters: '{0}'".format(commandText)
      args = commandText.split(',', 2)
      print 'args : ', args
      
      self.telescopeRa = self.raConversion.fromCgem(args[0])
      print 'self.telescope RA : ', self.telescopeRa
      
      self.telescopeDec = self.decConversion.fromCgem(args[1])
      print 'self.telescope.Dec : ', self.telescopeDec
      
      ser.write("#")
    elif prefix == 'K':
        argument = ser.read(1)
        ser.write (argument + '#')
    elif prefix == 'L':
        ser.write ('0#')
    elif prefix == 'e':
        # TODO: Store values from GOTO command (r/R) and return that here
        ser.write ('1234AB00,5678CD00#')
    else:
        print "Unknown command"

if __name__ == '__main__':
  done = False
  sim = TelescopeSim()
  
  while not done:
    cmd = ser.read(1)
    if cmd != '':
      print "Read command-char '{0}'".format(cmd)
      sim.parse_command(cmd)
    if cmd == 'q':
      print "Ready to quit"
      done = True

