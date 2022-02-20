import os
import cv2 as cv
import imutils
import numpy

class CameraService():
    def __init__(self):
        if os.environ.get("FLASK_ENV") == "production":
            self.camera = cv.VideoCapture(0)
        else:
            self.camera = cv.VideoCapture("./app-backend/media/video_sample.mp4")
        self.camera.set(cv.CAP_PROP_BUFFERSIZE, 1)

    def __del__(self):
        self.camera.release()

    def get_feed(self):
        while True:
            success, frame = self.camera.read()

            if not success:
                self.camera.set(cv.CAP_PROP_POS_FRAMES, 0)
                continue

            camera_width = int(os.environ.get("DEFAULT_CAMERA_WIDTH"))
            frame = imutils.resize(frame, width=camera_width)

            flag, encoded_frame = cv.imencode('.jpg', frame)

            if not flag:
                continue

            output_frame = bytearray(encoded_frame)

            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + output_frame + b'\r\n')

    def get_frame(self):
        if os.environ.get("FLASK_ENV") == "development":
            image = cv.imread(cv.samples.findFile("./app-backend/Flow/Base da dados/Pi camera/PCB_009.png"))
            return image

        success, frame = self.camera.read()

        if not success:
            return None

        flag, encoded_frame = cv.imencode('.png', frame)

        if not flag:
            return None

        bytes_as_np_array = numpy.frombuffer(encoded_frame, dtype=numpy.uint8)
        return cv.imdecode(bytes_as_np_array)