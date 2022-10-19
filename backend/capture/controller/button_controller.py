from gpiozero import Button
from flask import Blueprint, jsonify

button_blueprint = Blueprint('button_blueprint', __name__)
global pi_button
pi_button = Button(2)

@button_blueprint.route('/press',  methods = ['POST'])
def button_press():
    global pi_button

    pi_button.pin.drive_low()
    pi_button.pin.drive_high()

    return jsonify({"success": True})