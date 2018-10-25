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
        print 'About to kill null modem task'
        os.kill(self.pid_nullmodem,0)
        
if __name__ == '__main__':
    import time
    sp = SpawnSimulator()
    time.sleep(5)
    sp.shutdown()
    
    print 'exit'
    
