import time, json
from flask import render_template, Blueprint
from flask_sock import Sock, ConnectionClosed

analysis_blueprint = Blueprint('analysis_blueprint', __name__)
sock = Sock(analysis_blueprint)

@analysis_blueprint.route('/')
def index():
    return render_template('index.html')

@sock.route('/analysis')
def analysis(sock):
    try:
        print(f'Starting analysis websocket route...')
        counter = 1
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