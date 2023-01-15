from datetime import datetime
from threading import Thread
from database import Service
from ftp_server import FTPServer
from knn_classifier import KNNClassifier

import os
import shutil
import cv2 
import requests
import time

class Inference(Thread):
    def __init__(self, http, root):
        Thread.__init__(self)
        
        self.root = root
        self.http = http
        self.stop = False

    def preprocess_video(self, folder, video):
        video_cap = cv2.VideoCapture(video)
        success, image = video_cap.read()
        
        frame = 0
        
        while success:
            cv2.imwrite(os.path.join(folder, str(frame).zfill(8) + '.jpg'), image)
            success, image = video_cap.read()
            
            frame += 1
    
    def create_descriptors(self, folder):
        frames = sorted(os.listdir(folder))
        files = []
        
        for frame in frames:
            files.append(('files', (frame, open(os.path.join(folder, frame), 'rb'), 'image/jpeg')))
        
        payload={}
        headers = {}
        
        response = requests.request('POST', self.http + '/createmultidescriptors', headers=headers, data=payload, files=files)
        
        if response.status_code == 200:
            return response.json()
        
        return False
    
    def register_log(self, employee_id):
        db = Service('biometrica.db')
        
        query = """SELECT access_level 
                    FROM employees, roles
                    WHERE employees.role_id = roles.id
                    AND employees.id = {}""".format(employee_id)
        
        cursor, info = db.select(query)
        
        access_level = info[0][0]
        authorized = access_level
            
        query = """INSERT INTO logs (employee_id, authorized, datetime)
                    VALUES (?, ?, ?)"""
        data = (employee_id, authorized, str(datetime.now()).split('.')[0])
        
        db.insert(query, data)
        
        db.close()
    
    def run(self):
        self.ftp = FTPServer('192.168.0.217', 'esp', 'esp')
        
        time.sleep(30)
        
        while(not self.stop):
            self.ftp.get_videos()
            videos = os.listdir('videos')
            
            for video in videos:
                folder = os.path.join('videos', video.split('.')[0])
                os.mkdir(folder)
                
                self.preprocess_video(folder, os.path.join('videos', video))
                
                descriptors = self.create_descriptors(folder)
                
                shutil.rmtree(folder)
                
                if not descriptors:
                    os.remove(os.path.join('videos', video))
                    continue 
                
                descriptors = list(descriptors['list'])
                identified = set()

                for descriptor in descriptors:
                    knn = KNNClassifier(1, str(descriptor), 1000)
                    detected_id = knn.classify()
                    
                    if not detected_id in identified:
                        self.register_log(detected_id)
                        identified.add(detected_id)
                
                shutil.copyfile(os.path.join('videos', video), 'assets/lastdetection.avi')
                os.remove(os.path.join('videos', video))
            
                if len(video) != 0:
                    self.root.update_logs()
            
            time.sleep(30)