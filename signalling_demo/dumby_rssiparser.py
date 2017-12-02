import os
import threading
import time
import random as rand

class BluetoothRanger(threading.Thread):
    def __init__(self,_tags,_threshold):
        super(BluetoothRanger, self).__init__()
        #state variable intialization
        self.in_range = False

    def run(self):
        while True:
            time.sleep(0.1)
            self.in_range = rand.randint(0, 1) == 1
