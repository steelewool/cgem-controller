import serial

ser = serial.Serial('/dev/ttyUSB0')  # open serial port
print(ser.name)         # check which port was really used
char = ser.read()       # read a character
print 'char: ', char    # print the output
ser.close()             # close port
