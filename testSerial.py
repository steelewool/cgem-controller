import serial
import cgemInterface

ser = serial.Serial(port='./pty1', timeout=5)

cgemInterface = cgemInterface.CgemInterface(True)

ser.write(r'r39DDDD00,1ED80000')
print "Response:", ser.read(1)
ser.write(r'L')
print "Response:", ser.read(2)
# For now, embed the close command in here
# Eventually, the testbed should spawn/close the null modem & simulator
ser.write('q')
