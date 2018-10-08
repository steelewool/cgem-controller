import serial
import convertRaDecToCgemUnits
# Another neat idea would be to have this script spawn the virtual serial port
ser = serial.Serial(
    port = './pty2',
    timeout=1)

class TelescopeSim:
  lastRa  = convertRaDecToCgemUnits.Ra()
  lastDec = convertRaDecToCgemUnits.Dec()
  
  def parse_command(self, prefix):
    if prefix == 'r':
      commandText = ser.read(20)
      print "Read command parameters: '{0}'".format(commandText)
      args = commandText.split(',', 2)
      print 'args', args, args[0], args[1]
      x = self.lastRa.fromCgem(args[0])
      print 'x', x
      y = self.lastDec.fromCgem(args[1])
      print 'y', y
      ser.write("#")
    elif prefix == 'K':
        argument = ser.read(1)
        ser.write (argument + '#')
    elif prefix == 'L':
        ser.write ('0#')
    elif prefix == 'e':
        # TODO: Store values from GOTO command (r/R) and return that here
        print 'RA  : ', self.lastRa.toCgem()
        print 'Dec : ', self.lastDec.toCgem()
        #ser.write (self.lastRa.toCgem()+','+self.lastDec.toCgem()+'#')
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

