from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2
import random as rand


tol = 40
pix_check = 4000
res_x = 550
res_y = 200
motion_count = 0
average_y = res_y/2
status = "none"
def process_image(prior_img_data, img_data):
    global motion_count
    global average_y
    global status
    #global res_y
    if prior_img_data == None: return
    for i in range(pix_check):
        x = rand.randint(0, res_x - 1)
        y = rand.randint(0, res_y - 1)
        l = rand.randint(0, 2)
        prior_pixel = prior_img_data[y][x][l]
        pixel = img_data[y][x][l]
        if prior_pixel + tol < pixel or prior_pixel - tol > pixel:
            if y > res_y/2: #motions detected on the outside
                if status == "inside":
                    print "exiting"
                status = "outside"
            else:
                if status == "outside":
                    print "entering"
                status = "inside"
            motion_count += 1
            return True
    return False
        
def detect_motion_process():
    #launches camera
    global status
    global average_y
    camera = PiCamera()
    camera.resolution = (res_x, res_y)
    camera.framerate = 45
    rawCapture = PiRGBArray(camera, size = (res_x, res_y))
    prior_image_data = None
    time.sleep(0.1)
    no_motion_count = 0
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True):
        
        image = frame.array
        image_data = np.asarray(image)
        
        cv2.imshow("Frame", image)
        if process_image(prior_image_data, image_data):
            no_motion_count = 0
        prior_image_data = image_data
        key = cv2.waitKey(1)&0xFF
        
        #clear the stream  (prepare for next frame)
        rawCapture.truncate(0)
        
        if no_motion_count > 3:
            print "no motion clearing"
            average_y = res_y/2
            status = "none"
            no_motion_count = 0
        else:
            no_motion_count += 1
        
        if key == ord("q"):
            break

detect_motion_process()