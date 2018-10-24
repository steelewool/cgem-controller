# Provide basic goto operations for a manually entered RA/Declination

import os

class SpawnSimulator:
    def __init__(self):
        pid = os.spawnlp(os.P_NOWAIT, "python", "", "simulator.py")
        print 'simulator started'
        
if __name__ == '__main__':
    import time
    SpawnSimulator()
    time.sleep(120)
    print 'exit'
    