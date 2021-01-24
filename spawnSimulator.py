
import os
import signal
import time

# Kicks off either the nullmodem.sh script or debugTty.sh
# The debugTty.sh script is used for debugging hardware.
# The nullModem.sh and simulatory.py are using when running the simulator.

class SpawnSimulator:

    # Initializer for starting either nullmodem and simulator or
    # debugTty.sh.
    
    def __init__(self, simulate=True):

        print ('in SpawnSimulator __init__')

        self.simulate = simulate
        if self.simulate == True:

            print ('Spawn nullmodem.sh with P_NOWAIT')
            
            self.pid_modem = os.spawnlp(os.P_NOWAIT,
                                        "./nullmodem.sh", " ", " ")

            # Check that both pty1 and pty2 files exist before continuing

            print ('Check file existance.')
            
            checkFileExistance = True
            while checkFileExistance:
                checkFileExistance1 = os.path.exists("pty1")
                checkFileExistance2 = os.path.exists("pty2")
                checkFileExistance  = not(checkFileExistance1 and
                                          checkFileExistance2)

            print ('spawn python3')
            self.pid_python = os.spawnlp(os.P_NOWAIT,
                                         "python3", " ", "simulator.py")
        else:
            print ('spawn debugTty.sh')
            
            self.pid_modem = os.spawnlp(os.P_NOWAIT,
                                            "./debugTty.sh", " ", " ")

            print ('done spawing debugTty.sh')
            
            # Check that both pty1 and /dev/ttyUSB0 exists before continuing
            print ('Checking file existance.')
            
            checkFileExistance = True
            while checkFileExistance:
                checkFileExistance1 = os.path.exists("pty1")
                checkFileExistance2 = os.path.exists("/dev/ttyUSB0")
                checkFileExistance  = not(checkFileExistance1 and
                                          checkFileExistance2)
        print ('about to exit spawnSimulator initialization.')

    def shutdown(self):
        print ('shutdown running')
        if self.simulate == True:
#            time.sleep(1)
            os.kill(self.pid_python, signal.SIGSTOP)
        os.kill(self.pid_modem, signal.SIGSTOP);

if __name__ == '__main__':
    print ('invoke SpawnSimulator')
    sp = SpawnSimulator(True)
    print ('SpawnSimulator, sleep 5')
    time.sleep(5)
    sp.shutdown()


