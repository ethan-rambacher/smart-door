from motion_sensor import MotionSensor

class SmartDoor(object):
    def __init__(self):
        self.ms = MotionSensor(75, 40, 560, 160, 10, 10, False, self.motion_detected)
    
    def motion_detected(self):
        
    
    def run(self):
        self.ms.start()
    

sd = SmartDoor()
sd.run()
