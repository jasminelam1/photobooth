import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np

class RPiCamera(object):

    def __init__(self):
        self.stream = PiVideoStream().start()
        time.sleep(2.0)

    def __del__(self):
        self.stream.stop()

    def get_frame(self):
        frame = self.stream.read()
        cv2.imwrite("image.jpg", frame)
        result, jpeg = cv2.imencode('.jpg', frame)


        return jpeg