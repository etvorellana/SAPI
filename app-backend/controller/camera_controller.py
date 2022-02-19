import time
from service.camera_service import CameraService
from flask import Blueprint, Response

camera_blueprint = Blueprint('camera_blueprint', __name__)

@camera_blueprint.route('/feed')
def camera_feed():
    camera_service = CameraService()
    time.sleep(2)
    frame = camera_service.get_frame()
    return Response(frame, mimetype = "multipart/x-mixed-replace; boundary=frame")