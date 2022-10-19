import os
import time
import cv2 as cv
import imutils

class CameraService():
    def __init__(self):
        self.camera = cv.VideoCapture(0)
        self.camera.set(cv.CAP_PROP_BUFFERSIZE, 1)

    def __del__(self):
        self.camera.release()

    def get_feed(self):
        while True:
            camera_width = int(os.environ.get("DEFAULT_CAMERA_WIDTH"))
            if self.camera.isOpened() and os.environ.get("USE_CAMERA") == "true":
                success, frame = self.camera.read()

                if not success:
                    self.camera.set(cv.CAP_PROP_POS_FRAMES, 0)
                    continue

                frame = imutils.resize(frame, width=camera_width)

                flag, encoded_frame = cv.imencode('.jpg', frame)

                if not flag:
                    continue

                output_frame = bytearray(encoded_frame)

                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + output_frame + b'\r\n')
                time.sleep(0.06)
            else:
                output_frame = cv.imread(cv.samples.findFile("./media/no-camera.png"))
                output_frame = imutils.resize(output_frame, width=camera_width)
                flag, encoded_frame = cv.imencode('.jpg', output_frame)
                output_frame = bytearray(encoded_frame)

                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + output_frame + b'\r\n')
                time.sleep(0.06)

    def get_frame(self):
        if not self.camera.isOpened() or os.environ.get("USE_CAMERA") == "false":
            image = cv.imread(cv.samples.findFile("./media/pcb-sample.png"))
            return image

        self.camera.set(cv.CAP_PROP_FRAME_WIDTH, 2592)
        self.camera.set(cv.CAP_PROP_FRAME_HEIGHT, 1952)
        success, frame = self.camera.read()

        if not success:
            return None

        cv.imwrite("./media/frame.png", frame)
        image = cv.imread(cv.samples.findFile("./media/frame.png"))
        return image