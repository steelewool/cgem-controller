# Provide basic goto operations for a manually entered RA/Declination

import os
import signal
import time

class SpawnSimulator:

    # Initializer for starting either nullmodem and simulator or
    # debugTty.sh.
    
    def __init__(self, simulate=True):
        self.simulate = simulate
        if self.simulate == True:
            self.pid_modem = os.spawnlp(os.P_NOWAIT,
                                        "./nullmodem.sh", "", "")
            time.sleep(1)
            self.pid_python = os.spawnlp(os.P_NOWAIT,
                                         "python", "", "simulator.py")
        else:
            self.pid_modem = os.spawnlp(os.P_NOWAIT,
                                            "./debugTty.sh", "", "")

    def shutdown(self):
        if self.simulate == True:
            time.sleep(1)
            os.kill(self.pid_python, signal.SIGSTOP)
        os.kill(self.pid_modem, signal.SIGSTOP);

if __name__ == '__main__':
    sp = SpawnSimulator(True)
    time.sleep(5)
    sp.shutdown()


