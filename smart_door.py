from motion_sensor import MotionSensor

class SmartDoor(object):
    def __init__(self):
        self.ms = MotionSensor(75, 40, 160, 560, 10, 10, True, self.motion_detected, 0.8)
    
    def motion_detected(self):
        print "motion message delivered to system"
    
    def run(self):
        self.ms.start()
    

sd = SmartDoor()
sd.run()
