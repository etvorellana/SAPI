from flask import Blueprint, jsonify

button_blueprint = Blueprint('button_blueprint', __name__)

@button_blueprint.route('/press',  methods = ['POST'])
def button_press():
    from controller.analysis_controller import analysis_service

    analysis_service.pi_button.pin.drive_low()
    analysis_service.pi_button.pin.drive_high()

    return jsonify({"success": True})