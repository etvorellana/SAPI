import os
import imutils
from gpiozero import Button
from model.pcb_flow import PCBFlow
from service.state_service import StateService
from service.camera_service import CameraService
from view.flow import executar_flow
from util.img_util import from_np_array_to_base64

class AnalysisService:
    def __init__(self):
        self.pi_button = Button(2)
        self.button_pressed = False
        self.pi_button.when_released = self.button_released
        self.state_service = StateService()
        self.camera_service = CameraService()
        self.started = False
        self.frame_to_process = None
        self.image = None

    def orchestrate_state(self):
        state = self.state_service.state
        solders_state = None

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
            result_image, solders_state = self.orchestrate_analysis(self.frame_to_process)
            image_width = int(os.environ.get("DEFAULT_IMAGE_WIDTH"))
            self.image = imutils.resize(result_image, width=image_width)
            self.image = from_np_array_to_base64(self.image)
            self.state_service.change_state()
        
        result = {"state": state, "solders_state": solders_state, "image": self.image}
        return result

    def orchestrate_analysis(self, image):
        # orchestrate analysis
        print(f"Starting image analysis...")
        pcb_flow = PCBFlow(image)
        result_image = executar_flow(pcb_flow)
        solders_state = {}
        return result_image, solders_state

    def button_released(self):
        print(f'Button pressed!')
        if self.started:
            self.button_pressed = True