import serial

# Another neat idea would be to have this script spawn the virtual serial port
ser = serial.Serial(
    port = './pty2',
    timeout=1)

class TelescopeSim:
  
  def parse_command(self, prefix):
    if prefix == 'r':
      commandText = ser.read(20)
      print "Read command parameters: '{0}'".format(commandText)
      args = commandText.split(',', 2)
      ser.write("#")
    elif prefix == 'K':
        argument = ser.read(1)
        ser.write (argument + '#')
    elif prefix == 'L':
        ser.write ('0#')
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

