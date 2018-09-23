# This is using two serial to USB cables connected together with a
# null modem and gender bender connector. It worked on 9/10/2018.
# This has the disadvantage of using two usb ports and required two
# cables. But I feel it is more real life than the loop back test
# done with haywires.

import serial

ser = serial.Serial(port     = '/dev/ttyUSB0',
                     baudrate =          9600,
                     timeout  =             1) # open serial port

print 'ser.name : ', ser.name    # check which port was really used

ser.write(b'e')            # write a string

print 'read from serial port'

foundHashTag = True

output = ''

while (foundHashTag):
    data = ser.read(1)
    output = output + data
    if (data == '#'):
        foundHashTag = False
print 'output: ', output

ser.close()                     # close port

