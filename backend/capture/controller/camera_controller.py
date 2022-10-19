import time
from service.camera_service import CameraService
from flask import Blueprint, Response

camera_blueprint = Blueprint('camera_blueprint', __name__)
global camera_service
camera_service = CameraService()

@camera_blueprint.route('/feed')
def camera_feed():
    time.sleep(2)
    frame = camera_service.get_feed()
    return Response(frame, mimetype = "multipart/x-mixed-replace; boundary=frame")