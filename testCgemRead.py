# This is using two serial to USB cables connected together with a
# null modem and gender bender connector. It worked on 9/10/2018.
# This has the disadvantage of using two usb ports and required two
# cables. But I feel it is more real life than the loop back test
# done with haywires.

import serial

ser0 = serial.Serial('/dev/ttyUSB0',
                     baudrate = 9600,
                     timeout  =    6 ) # open serial port

print 'ser0.name : ', ser0.name    # check which port was really used

ser0.write(b'e')            # write a string

print 'read from serial port'

char = ser0.read(20)            # read a character

print 'char     : ', char       # print the output

ser0.close()                     # close port

