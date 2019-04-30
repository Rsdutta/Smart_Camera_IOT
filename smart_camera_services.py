import requests
import time
import cv2
from datetime import datetime
import dropbox
import os


class Cloud_Components:
    def __init__(self, mailgun_key, mailgun_sandbox, mailgun_recipient, dropbox_access_token):
        self.mailgun_key = mailgun_key
        self.mailgun_sandbox = mailgun_sandbox
        self.mailgun_recipient = mailgun_recipient
        self.dropbox_instance = dropbox.Dropbox(dropbox_access_token)
        self.mailgun_url = 'https://api.mailgun.net/v2/{}/messages'.format(self.mailgun_sandbox)    

    def upload_file(self, img, cam_number):
        name = '{}.png'.format(datetime.now().strftime("%m-%d-%Y, %H:%M:%S"))
        print name
        status = cv2.imwrite("test.jpg", img)
        with open('test.jpg', 'rb') as f:
            self.dropbox_instance.files_upload(f.read(), '/camera_{}/{}'.format(cam_number, name))
            print "sent"
        pass

    def send_email(self, cam_number, detection_type):
        request = requests.post(self.mailgun_url, auth=('api', self.mailgun_key), data={
            'from': 'Mailgun Sandbox <postmaster@{}>'.format(self.mailgun_sandbox),
            'to': self.mailgun_recipient,
            'subject': 'Suspicious Actions Detected',
            'text': 'Hello. Camera {} has detected {}. Frames are available on dropbox'.format(cam_number, detection_type)})
        print request
        pass









