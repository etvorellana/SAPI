import os
import time
import cv2 as cv
import imutils

class CameraService():
    def __init__(self):
        if os.environ.get("FLASK_ENV") == "production":
            self.camera = cv.VideoCapture(0)
        else:
            self.camera = cv.VideoCapture("./media/video_sample.mp4")
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
            time.sleep(0.06)

    def get_frame(self):
        if os.environ.get("FLASK_ENV") == "development":
            image = cv.imread(cv.samples.findFile("./Flow/Base da dados/Pi camera/PCB_009.png"))
            return image

        self.camera.set(cv.CAP_PROP_FRAME_WIDTH, 2592)
        self.camera.set(cv.CAP_PROP_FRAME_HEIGHT, 1952)
        success, frame = self.camera.read()

        if not success:
            return None

        cv.imwrite("./media/frame.png", frame)
        image = cv.imread(cv.samples.findFile("./media/frame.png"))
        return image