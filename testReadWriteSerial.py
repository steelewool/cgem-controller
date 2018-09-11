# This is using two serial to USB cables connected together with a
# null modem and gender bender connector. It worked on 9/10/2018.
# This has the disadvantage of using two usb ports and required two
# cables. But I feel it is more real life than the loop back test
# done with haywires.

import serial

ser0 = serial.Serial('/dev/ttyUSB0', timeout=1) # open serial port
# ser1 = serial.Serial('/dev/ttyUSB1', timeout=1) # open 2nd serial port

print 'ser0.name : ', ser0.name    # check which port was really used
# print 'ser1.name : ', ser1.name

print 'write hello from serial 0'

ser0.write(b'hello')            # write a string

print 'read from serial port'

char = ser0.read(20)            # read a character
# char = ser1.read(20)            # read a character

print 'char     : ', char       # print the output

ser0.close()                     # close port
# ser1.close()
