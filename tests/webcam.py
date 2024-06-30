import cv2
import os

web_cam = cv2.VideoCapture(0)

def webcam_capture():
    if not web_cam.isOpened():
        print('Error')
        exit()
    path = os.path.join(os.path.dirname(__file__), '../assets/video/webcam.jpg')
    ret, frame = web_cam.read()
    cv2.imwrite(path, frame)

webcam_capture()

