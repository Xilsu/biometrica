import os
import argparse
import cv2

class Preprocess:
    def __init__(self, path, video):
        self.path = path 
        self.video = video
    
    def preprocess_video(self):
            video_cap = cv2.VideoCapture(os.path.join(self.path, self.video))
            success, image = video_cap.read()

            folder = os.path.join(self.path, self.video[:-4])
            os.mkdir(folder)
            
            frame = 0
            
            while success:
                cv2.imwrite(os.path.join(folder, str(frame).zfill(8) + '.jpg'), image)
                success, image = video_cap.read()
                
                frame += 1

if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    
    argParser.add_argument('-p', '--path', help='video path')
    argParser.add_argument('-v', '--video', help='video file')

    args = argParser.parse_args()

    preprocess = Preprocess(args.path, args.video)
    preprocess.preprocess_video()