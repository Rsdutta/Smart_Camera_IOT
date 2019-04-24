import cv2
from motion import BasicMotionDetector
import time
import datetime
import numpy as np
import sys


class smart_camera(object):
    def __init__(self, tracking_type, cam_number):
        self.capture = cv2.VideoCapture(cam_number)
        self.capture.set(3, 480)
        self.capture.set(4, 360)
        self.tracking_type = tracking_type
        self.basic_motion = BasicMotionDetector()
        self.faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.cam_number = cam_number

    def get_processed_frame(self):
        ret, img = self.capture.read()
        if 'face' in self.tracking_type:
            return self.face_detection(img)
        else:
            return self.motion_tracking(img)


    def motion_tracking(self, img):
        if self.cam_number == 0:
            cam_num = 1
        else:
            cam_num = 2
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        locs = self.basic_motion.update(gray)
        if len(locs) > 0:
            # initialize the minimum and maximum (x, y)-coordinates,
            # respectively
            (minX, minY) = (np.inf, np.inf)
            (maxX, maxY) = (-np.inf, -np.inf)

            # loop over the locations of motion and accumulate the
            # minimum and maximum locations of the bounding boxes
            for l in locs:
                (x, y, w, h) = cv2.boundingRect(l)
                (minX, maxX) = (min(minX, x), max(maxX, x + w))
                (minY, maxY) = (min(minY, y), max(maxY, y + h))

            # draw the bounding box
            cv2.rectangle(img, (minX, minY), (maxX, maxY),
                (0, 0, 255), 3)
            
            # update the frames list

        # increment the total number of frames read and grab the 
        # current timestamp
        timestamp = datetime.datetime.now()
        ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
        cv2.putText(img, "Cam: " + str(cam_num), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(img, "Motion Tracking", (img.shape[0] - 70, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(img, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

        # loop over the frames a second time
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()
        #cv2.imshow("Motion Tracking " + str(self.cam_number), img)
    
    def face_detection(self, img):
        if self.cam_number == 0:
            cam_num = 1
        else:
            cam_num = 2
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(
            gray,     
            scaleFactor=1.2,
            minNeighbors=5, 
            minSize=(20, 20)
        )
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
        
        timestamp = datetime.datetime.now()
        ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
        cv2.putText(img, "Cam: " + str(cam_num), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(img, "Face Tracking", (img.shape[0] - 50, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(img, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()
        #cv2.imshow('Face Tracking ' + str(self.cam_number),img)

#cam1 = smart_camera("face", 0)
#cam2 = smart_camera("motion", 2)


#while True:
   #cam1.get_processed_frame()
 #   cam2.get_processed_frame()
    
  #  key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
   # if key == ord("q"):
    #    break

