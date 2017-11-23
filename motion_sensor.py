from picamera.array import PiRGBArray
from picamera import PiCamera
import threading
import numpy as np
import time
import cv2
import random as rand

class MotionSensor(threading.Thread):
    
    def __init__(self, frame_rate, tol, res_x, res_y, step_x, step_y, show_camera, on_motion_call, time_thresh_hold):
        super(MotionSensor, self).__init__()
        #camera set up 
        self.camera = PiCamera()
        self.camera.resolution = (res_x, res_y)
        self.camera.framerate = frame_rate
        self.rawCapture = PiRGBArray(self.camera, size = (res_x, res_y))
        time.sleep(0.1)
        #iteration setup
        self.tol = tol
        self.res_x = res_x
        self.res_y = res_y
        self.step_x = step_x
        self.step_y = step_y
        #display camera on screen
        self.show_camera = show_camera
        self.on_motion_call = on_motion_call
        self.time_thresh_hold = time_thresh_hold
        self.loc_path = []
        
    def process_image(self, prior_img_data, img_data):
        if prior_img_data == None: return (-1, -1)
        for x in range(0, self.res_x, self.step_x):
            for y in range(0, self.res_y, self.step_y):
                l = (x*y>> 3)*13%3 #arbitrary hasher
                prior_pixel = prior_img_data[y][x][l]
                pixel = img_data[y][x][l]
                if prior_pixel + self.tol < pixel or prior_pixel - self.tol > pixel:
                    return (x, y)
        return (-1, -1)
    
    def run(self):
        prior_time = -50
        motion_count = 0
        prior_image_data = None
        #every iteration through is a new frame
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port = True):
            #speeding up image iteration
            image = frame.array
            image_data = np.asarray(image)
            if self.show_camera:
                cv2.imshow("Frame", image)
            
            x, y = self.process_image(prior_image_data, image_data)
            if x != -1: #a specific location was found
                current_time = time.time()
                if current_time - prior_time > self.time_thresh_hold:
                    last_p_y = None
                    dy_sum = 0
                    for p_x, p_y in self.loc_path:
                        if last_p_y == None:
                            last_p_y = p_y
                            continue
                        dy_sum += (last_p_y - p_y)
                    print dy_sum
                    self.loc_path = []
                self.on_motion_call()
                #actions that need to be taken when motion occures
                self.loc_path.append((x, y))
                print str(motion_count) + ": MOTION!                      " + str(time.time()) + " loc: " + str(x) +", " + str(y)
                motion_count += 1
                prior_time = current_time
                
            prior_image_data = image_data
            
            self.rawCapture.truncate(0) #clear the stream (prepare for next frame)
            
            if self.show_camera:
                key = cv2.waitKey(1)&0xFF       
                if key == ord("q"):
                    break