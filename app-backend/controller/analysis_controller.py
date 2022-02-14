import json, time
from flask import Blueprint
from flask_sock import Sock, ConnectionClosed
from gpiozero import Button

analysis_blueprint = Blueprint('analysis_blueprint', __name__)
sock = Sock(analysis_blueprint)
piButton = Button(2)

@sock.route('')
def analysis(sock):
    try:
        print(f'Starting analysis websocket route...')
        counter = 1
        piButton.when_released = button_released
        while True:
            message = json.dumps({"message": f'hello {counter}'})
            sock.send(message)
            counter += 1
            print(f'Hello sent. Waiting until next message...')
            time.sleep(2)
    except ConnectionClosed as ex:
        print(f"Connection terminated by the client. {ex}")
    except Exception as ex:
        print(f"Unexpected error occurred. {ex}")

def button_released():
    print(f'Button pressed!')