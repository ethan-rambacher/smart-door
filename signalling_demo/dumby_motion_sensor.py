import threading
import numpy as np
import time
import random as rand

class MotionSensor(threading.Thread):

    def __init__(self, frame_rate, tol, res_x, res_y, step_x, step_y, show_camera, on_motion_call, time_thresh_hold):
        super(MotionSensor, self).__init__()
        self.on_motion_call = on_motion_call
        self.res_x = res_x
        self.res_y = res_y

    def process_image(self, prior_img_data, img_data):
        pass

    def run(self):
        while True:
            x = 1
            y = 1
            time.sleep(5)
            self.on_motion_call(rand.randint(0, self.res_x - 1), rand.randint(0, self.res_y - 1))
