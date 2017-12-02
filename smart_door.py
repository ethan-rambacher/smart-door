from motion_sensor import MotionSensor
from rssiparser import BluetoothRanger
import os

class SmartDoor(object):
    def __init__(self):
        self.ms = MotionSensor(75, 40, 1000, 1000, 20, 20, True, self.motion_detected, 0.8)
        self.thresh_hold_x = 500
        #self.people_in_range = False
        #self.bt_buffer = os.popen("sudo hcidump & sudo hcitool lescan --duplicates")
        self.br = BluetoothRanger({"FF:FF:80:00:86:56"},-80)

    def motion_detected(self, x, y):
        if x > self.thresh_hold_x:
            print "EXIT: " + str(x)
            print "BT in range: " + str(self.br.in_range)
        else:
            print "ENTER: " + str(x)
            print "BT in range: " + str(self.br.in_range)

    def run(self):
        self.ms.start()
        self.br.start()


sd = SmartDoor()
sd.run()
