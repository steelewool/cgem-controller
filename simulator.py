import serial

# Another neat idea would be to have this script spawn the virtual serial port
ser = serial.Serial(
    port = './pty2',
    timeout=1)


def parse_command(prefix):
  if prefix == 'r':
    commandText = ser.read(20)
    print "Read command parameters: '{0}'".format(commandText)
    ser.write("#")
  else:
    print "Unknown command"

done = False

while not done:
  cmd = ser.read(1)
  if cmd != '':
    print "Read command-char '{0}'".format(cmd)
    parse_command(cmd)
  if cmd == 'q':
    print "Ready to quit"
    done = True

