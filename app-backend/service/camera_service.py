import os
import cv2 as cv
import imutils

class CameraService():
    def __init__(self):
        if os.environ.get("FLASK_ENV") == "production":
            self.camera = cv.VideoCapture(0)
        else:
            self.camera = cv.VideoCapture("./app-backend/media/video_sample.mp4")
        self.camera.set(cv.CAP_PROP_BUFFERSIZE, 1)

    def __del__(self):
        self.camera.release()

    def get_frame(self):
        while True:
            success, frame = self.camera.read()

            if not success:
                self.camera.set(cv.CAP_PROP_POS_FRAMES, 0)
                continue

            frame = imutils.resize(frame, width=1024)

            flag, encoded_frame = cv.imencode('.jpg', frame)

            if not flag:
                continue

            output_frame = bytearray(encoded_frame)

            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + output_frame + b'\r\n')