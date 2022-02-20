import json
import time
from flask import Blueprint
from flask_sock import Sock, ConnectionClosed
from service.analysis_service import AnalysisService

analysis_blueprint = Blueprint('analysis_blueprint', __name__)
sock = Sock(analysis_blueprint)
analysis_service = AnalysisService()

@sock.route('')
def analysis(sock):
    try:
        print(f'Starting analysis websocket route...')
        analysis_service.started = True
        analysis_service.state_service.set_state(1)

        while True:
            result = analysis_service.orchestrate_state()
            # state 1 - start of process
            # state 2 - watching camera
            # state 3 - processing image start
            # state 4 - processing image finished
            # state 5 - showing image and waiting for restart
            if result['state'] == 1 or result['state'] == 3 or result['state'] == 4: # only these states are sent to client
                message_json = json.dumps(result)
                print(f"Sending message for state: {result['state']}")
                sock.send(message_json)
            time.sleep(0.1)

    except ConnectionClosed as ex:
        print(f"Connection terminated by the client. {ex}")
    except Exception as ex:
        print(f"Unexpected error occurred. {ex}")
    
    analysis_service.started = False