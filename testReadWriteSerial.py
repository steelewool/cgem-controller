import serial

ser = serial.Serial('/dev/ttyUSB0', timeout=2)  # open serial port
print(ser.name)         # check which port was really used
ser.write(b'hello')     # write a string

char = ser.read()       # read a character
print 'char: ', char    # print the output

ser.close()             # close port
