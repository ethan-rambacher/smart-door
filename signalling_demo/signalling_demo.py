from dumby_motion_sensor import MotionSensor
from dumby_rssiparser import BluetoothRanger
import os
import random as rand
import RPi.GPIO as GPIO

class SmartDoor(object):
    def __init__(self):
        self.ms = MotionSensor(75, 40, 1000, 1000, 20, 20, False, self.motion_detected, 0.8)
        self.thresh_hold_x = 500
        self.br = BluetoothRanger({"FF:FF:80:00:86:56"},-80)
        self.led_pin = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin,GPIO.OUT)

    def motion_detected(self, x, y):
        print "Signalling Subsytem Recieved Camera Notification"
        if(self.br.in_range):
            print "Tag Status: NEARBY "
        else:
            print "Tag Status: FAR AWAY"

        if x > self.thresh_hold_x: #attemtping to exit the room
            print "    Motion: EXITING"
            if not self.br.in_range: #tag status is far away
                self.alert()
        else:
            print "    Motion: ENTERING"
        print "#"*50
        print "\n"*5

    def alert(self):
        print "\n$$$ Sending Flag to Alert Subsystem $$$"
        GPIO.output(self.led_pin, GPIO.HIGH)
        os.system("mplayer leave_room.m4a > stupid_data.txt")
        GPIO.output(self.led_pin, GPIO.LOW)


    def run(self):
        self.ms.start()
        self.br.start()


sd = SmartDoor()
sd.run()
