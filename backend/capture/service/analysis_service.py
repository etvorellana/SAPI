import base64
import io
import os
import threading
import time

import cv2 as cv
import imutils
import numpy
import requests
from PIL import Image
from util.img_util import from_np_array_to_base64

import service.filter_service as filter_service
from service.state_service import StateService


class AnalysisService:
    def __init__(self):
        from controller.button_controller import pi_button
        self.button_pressed = False
        pi_button.when_released = self.button_released
        self.state_service = StateService()
        from controller.camera_controller import camera_service
        self.camera_service = camera_service
        self.started = False
        self.frame_to_process = None
        self.image = None
        self.result = None
        self.classification = None
        self.lock = threading.Lock()

    def start(self):
        while True:
            if self.started:
                self.result = self.orchestrate_state()
            time.sleep(0.10001)

    def orchestrate_state(self):
        with self.lock:
            try:
                state = self.state_service.state
                solders_classification = None

                if self.button_pressed:
                    self.state_service.change_state()
                    self.button_pressed = False

                if state == 1:
                    self.image = None
                    self.state_service.change_state()
                elif state == 3:
                    self.frame_to_process = self.camera_service.get_frame()
                    image_width = int(os.environ.get("DEFAULT_IMAGE_WIDTH"))
                    self.image = imutils.resize(self.frame_to_process, width=image_width)
                    self.image = from_np_array_to_base64(self.image)
                    self.state_service.change_state()
                elif state == 4:
                    if self.frame_to_process is None:
                        print("No frame set for analysis!")
                        raise RuntimeError("Unable to acquire frame for analysis.")
                    result_image, solders_classification = self.orchestrate_analysis(self.frame_to_process)
                    image_width = int(os.environ.get("DEFAULT_IMAGE_WIDTH"))
                    self.image = imutils.resize(result_image, width=image_width)
                    self.image = from_np_array_to_base64(self.image)
                    self.classification = solders_classification
                    self.state_service.change_state()

                result = {"state": state, "solders_classification": self.classification, "image": self.image}
                return result
            except Exception as ex:
                print(f"Error during orchestrate state: {ex}")
                self.state_service.set_state(2)
                result = {"state": 2, "solders_classification": None, "image": None}
                return result

    def orchestrate_analysis(self, image):
        # orchestrate analysis
        print(f"Calling remote image analysis...")
        url = os.environ.get("ANALYSIS_ENDPOINT")
        payload = { "image": from_np_array_to_base64(image), "filter": filter_service.current_filter }
        result = requests.post(url, json = payload)
        if (not result.ok):
            raise RuntimeError("Received error response from remote analysis server")
        img_data = base64.b64decode(result.json()["image"])
        pil_img = Image.open(io.BytesIO(img_data))
        img = cv.cvtColor(numpy.array(pil_img), cv.COLOR_BGR2RGB)
        return img, result.json()["classification"]

    def button_released(self):
        print(f'Button pressed!')
        if self.started:
            self.button_pressed = True
