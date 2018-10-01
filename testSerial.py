import serial

ser = serial.Serial(port='./pty1', timeout=5)

ser.write(r'r39DDDD00,1ED80000')
print "Response:", ser.read(1)
# For now, embed the close command in here
# Eventually, the testbed should spawn/close the null modem & simulator
ser.write('q')
