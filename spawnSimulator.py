# Provide basic goto operations for a manually entered RA/Declination

import os
import signal
import time

class SpawnSimulator:

    def __init__(self):
        self.pid_nullmodem = os.spawnlp(os.P_NOWAIT, "./nullmodem.sh", "", "")
        time.sleep(1)
        self.pid_python = os.spawnlp(os.P_NOWAIT, "python", "", "simulator.py")
        print 'simulator started'
    def shutdown(self):
        print 'About to kill null modem task - kill not working'
        os.kill(self.pid_nullmodem,signal.SIGINT)
        time.sleep(1)
#        os.kill(self.pid_python,   signal.SIGINT)
        
if __name__ == '__main__':
    sp = SpawnSimulator()
    time.sleep(5)
    sp.shutdown()
    
    print 'exit'
    
