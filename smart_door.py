from motion_sensor import MotionSensor

class SmartDoor(object):
    def __init__(self):
        self.ms = MotionSensor(75, 40, 1000, 1000, 20, 20, False, self.motion_detected, 0.8)
        self.thresh_hold_x = 500
    
    def motion_detected(self, x, y):
        if x > self.thresh_hold_x:
            print "EXIT: " + str(x)
        else:
            print "ENTER: " + str(x)
    
    def run(self):
        self.ms.start()
    

sd = SmartDoor()
sd.run()
