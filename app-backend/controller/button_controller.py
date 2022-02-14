from flask import Blueprint, jsonify

button_blueprint = Blueprint('button_blueprint', __name__)

@button_blueprint.route('/press',  methods = ['POST'])
def index():
    from controller.analysis_controller import piButton
    piButton.pin.drive_low()
    piButton.pin.drive_high()
    return jsonify({"success": True})