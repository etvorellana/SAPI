import base64
import cv2 as cv
from gpiozero import Button
from service.state_service import StateService
from service.camera_service import CameraService

class AnalysisService:
    def __init__(self):
        self.pi_button = Button(2)
        self.button_pressed = False
        self.pi_button.when_released = self.button_released
        self.state_service = StateService()
        self.camera_service = CameraService()
        self.started = False

    def orchestrate_state(self):
        state = self.state_service.state
        processed_image = None

        if self.button_pressed:
            self.state_service.change_state()
            self.button_pressed = False

        if state == 1:
            self.state_service.change_state()
        elif state == 3:
            frame = self.camera_service.get_frame()
            processed_image = self.orchestrate_analysis(frame)
            self.state_service.change_state()
        
        result = {"state": state, "image": processed_image}
        return result

    def orchestrate_analysis(self, image):
        # orchestrate analysis
        print(f"Starting image analysis...")
        file_image = cv.imread(cv.samples.findFile("./app-backend/Flow/Base da dados/Pi camera/PCB_001.png"))
        base64bytes = base64.b64encode(file_image)
        image_string = base64bytes.decode("ascii")
        resultImage = image_string
        return resultImage

    def button_released(self):
        print(f'Button pressed!')
        if self.started:
            self.button_pressed = True