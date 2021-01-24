import serial
import spawnSimulator
import cgemInterface
import time

if __name__ == '__main__':
    
    # Request input as to if simulation or using telescope hardware
    
    if input("Enter 1 for simulation 2 for hardware ") == '1':
        simulate = True
        print ('Simulate set to true')
    else:
        simulate = False
        print ('Simulate set to false')

    sp = spawnSimulator.SpawnSimulator(simulate)

    cgemInterface = cgemInterface.CgemInterface()

    cgemInterface.echoCommand('a')
    
    # Done - shut down and clean up

    time.sleep(5)

    print ('Quitting, closing simulator, and serial interfaces.')

    cgemInterface.quitSimulator() # does nothing when operating with telescope
    cgemInterface.closeSerial()
    sp.shutdown()

# OLD CODE:

#ser = serial.Serial(port='./pty1', timeout=5)

#cgemInterface = cgemInterface.CgemInterface(True)

#ser.write(r'r39DDDD00,1ED80000')
#print ('Response:', ser.read(1))
#ser.write(r'L')
#print ('Response:', ser.read(2))
# For now, embed the close command in here
# Eventually, the testbed should spawn/close the null modem & simulator
#ser.write('q')
