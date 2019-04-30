import cv2
from motion import BasicMotionDetector
import time
import datetime
import numpy as np
import sys
from smart_camera_services import Cloud_Components
from threading import Thread

cloud_service = Cloud_Components('b3d30542a678bdc4b324adadbda35283-dc5f81da-74721564', 'sandbox24ef91fac1c64d1c976dfe3e8b912b18.mailgun.org', 'Rishov Dutta <rsdutta2@illinois.edu>', 'DhHEQ1Ie2qAAAAAAAAAACZ_zsdvAzb8kungzHGW-yg4VlMjxA4d7PIvK1MH1_eGW')
class smart_camera(object):
    def __init__(self, tracking_type, cam_number):
        self.capture = cv2.VideoCapture(cam_number)
        self.capture.set(3, 480)
        self.capture.set(4, 360)
        self.tracking_type = tracking_type
        self.basic_motion = BasicMotionDetector()
        self.faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.cam_number = cam_number
        self.smart_camera_email = 0
        self.smart_camera_dropbox = 0

    def get_processed_frame(self):
        ret, img = self.capture.read()
        if 'face' in self.tracking_type:
            return self.face_detection(img)
        else:
            return self.motion_tracking(img)


    def motion_tracking(self, img):
        detection_flag = False
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
            detection_flag = True
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
        if detection_flag:
            if time.time() - self.smart_camera_email > 300 or self.smart_camera_email == 0:
                self.smart_camera_email = time.time()
                Thread(target=cloud_service.send_email, args=(self.cam_number, self.tracking_type)).start()
            if time.time() - self.smart_camera_dropbox > 1.5 or self.smart_camera_dropbox == 0:
                self.smart_camera_dropbox = time.time()
                Thread(target=cloud_service.upload_file, args=(img, self.cam_number)).start()
        ret, jpeg = cv2.imencode('.jpg', img)
        cv2.imwrite("wtf.jpg", img)
        return jpeg.tobytes()
    
    def face_detection(self, img):
        detection_flag = False
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
            detection_flag = True
        
        timestamp = datetime.datetime.now()
        ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
        cv2.putText(img, "Cam: " + str(cam_num), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(img, "Face Tracking", (img.shape[0] - 50, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(img, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)
        if detection_flag:
            if time.time() - self.smart_camera_email > 300 or self.smart_camera_email == 0:
                self.smart_camera_email = time.time()
                Thread(target=cloud_service.send_email, args=(self.cam_number, self.tracking_type)).start()
            if time.time() - self.smart_camera_dropbox > 5 or self.smart_camera_dropbox == 0:
                self.smart_camera_dropbox = time.time()
                Thread(target=cloud_service.upload_file, args=(img, self.cam_number)).start()
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()
        