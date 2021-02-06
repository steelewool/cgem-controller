
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

        self.simulate = simulate
        if self.simulate == True:
            self.pid_modem = os.spawnlp(os.P_NOWAIT,
                                        "./nullmodem.sh", " ", " ")
            
            # Check that both pty1 and pty2 files exist before continuing
            # Appears that nullmodem.sh creates the pty1 and pty2 files.
            # But I want to check with Zach to see if he remembers this
            # part of the code.
            
            checkFileExistance = True
            while checkFileExistance:
                checkFileExistance1 = os.path.exists("pty1")
                checkFileExistance2 = os.path.exists("pty2")
                checkFileExistance  = not(checkFileExistance1 and
                                          checkFileExistance2)

            self.pid_python = os.spawnlp(os.P_NOWAIT,
                                         "python3", " ", "simulator.py")

            time.sleep(2)
        else:

            self.pid_modem = os.spawnlp(os.P_NOWAIT,
                                            "./debugTty.sh", " ", " ")
            
            # Check that both pty1 and /dev/ttyUSB0 exists before continuing
            
            checkFileExistance = True
            while checkFileExistance:
                checkFileExistance1 = os.path.exists("pty1")
                checkFileExistance2 = os.path.exists("/dev/ttyUSB0")
                checkFileExistance  = not(checkFileExistance1 and
                                          checkFileExistance2)
    def shutdown(self):
        if self.simulate == True:
            os.kill(self.pid_python, signal.SIGSTOP)
        os.kill(self.pid_modem, signal.SIGSTOP);

if __name__ == '__main__':
    sp = SpawnSimulator(True)
    time.sleep(5)
    sp.shutdown()


