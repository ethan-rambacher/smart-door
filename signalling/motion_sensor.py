from picamera.array import PiRGBArray
from picamera import PiCamera
import threading
import numpy as np
import time
import cv2
import random as rand

class MotionSensor(threading.Thread):
    
    def __init__(self, frame_rate, tol, res_x, res_y, step_x, step_y, show_camera):
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
        
        #motion flag
        self.motion_flag = False
        
    def process_image(self, prior_img_data, img_data):
        if prior_img_data == None: return False
        for x in range(0, self.res_x, self.step_x):
            for y in range(0, self.res_y, self.step_y):
                l = (x*y>> 3)*13%3 #arbitrary hasher
                prior_pixel = prior_img_data[y][x][l]
                pixel = img_data[y][x][l]
                if prior_pixel + self.tol < pixel or prior_pixel - self.tol > pixel:
                    return True
        return False
    
    def run(self):
        motion_count = 0
        prior_image_data = None
        #every iteration through is a new frame
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port = True):
            #speeding up image iteration
            image = frame.array
            image_data = np.asarray(image)
            if self.show_camera:
                cv2.imshow("Frame", image)
                
            if self.process_image(prior_image_data, image_data):
                self.motion_flag = True
                #actions that need to be taken when motion occures
                print str(motion_count) + ": MOTION!"
                motion_count += 1
                
            prior_image_data = image_data
            
            self.rawCapture.truncate(0) #clear the stream (prepare for next frame)
            
            if self.show_camera:
                key = cv2.waitKey(1)&0xFF       
                if key == ord("q"):
                    break


ms = MotionSensor(75, 40, 550, 150, 10, 10, True)
ms.start()


'''

tol = 40
res_x = 550
res_y = 150
step_x = 10
step_y = 10

def process_image(prior_img_data, img_data):
    if prior_img_data == None: return
    for x in range(0, res_x, step_x):
        for y in range(0, res_y, step_y):
            l = (x*y>> 3)*13%3 #arbitrary hasher
            prior_pixel = prior_img_data[y][x][l]
            pixel = img_data[y][x][l]
            if prior_pixel + tol < pixel or prior_pixel - tol > pixel:
                return True
    return False
        
def detect_motion_process():
    motion_count = 0
    
    #launches camera
    camera = PiCamera()
    camera.resolution = (res_x, res_y)
    camera.framerate = 75
    rawCapture = PiRGBArray(camera, size = (res_x, res_y))
    prior_image_data = None
    time.sleep(0.1)
    no_motion_count = 0
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True):
        
        image = frame.array
        image_data = np.asarray(image)
       
        cv2.imshow("Frame", image)
        if process_image(prior_image_data, image_data):
            print str(motion_count) + ": MOTION!"
            motion_count += 1
            
        prior_image_data = image_data
        key = cv2.waitKey(1)&0xFF
        
        #clear the stream  (prepare for next frame)
        rawCapture.truncate(0)

        if key == ord("q"):
            break

detect_motion_process()'''