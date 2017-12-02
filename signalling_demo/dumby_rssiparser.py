import os
import threading
import time

class BluetoothRanger(threading.Thread):
    def __init__(self,_tags,_threshold):
        super(BluetoothRanger, self).__init__()
        #state variable intialization
        self.in_range = False

    def run(self):
        while True:
            time.sleep(0.2)
            self.in_range = not self.in_range
