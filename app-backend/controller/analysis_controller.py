import json
import threading
import time
from flask import Blueprint
from flask_sock import Sock, ConnectionClosed
from service.analysis_service import AnalysisService

analysis_blueprint = Blueprint('analysis_blueprint', __name__)
sock = Sock(analysis_blueprint)
analysis_service = AnalysisService()
analysis_thread = threading.Thread(target=analysis_service.start, args=(), daemon=True)
analysis_thread.start()
global connection_count
connection_count = 0

@sock.route('')
def analysis(sock):
    global connection_count
    connection_count += 1

    try:
        if analysis_service.started:
            message_json = json.dumps(analysis_service.result)
            print("Client reconnected...")
            print(f"Sending message for state: {analysis_service.result['state']}")
            sock.send(message_json)
        else:
            print(f'Starting analysis websocket route...')
            analysis_service.started = True

        while True:
            with analysis_service.lock:
                result = analysis_service.result
                # state 1 - start of process
                # state 2 - watching camera
                # state 3 - processing image start
                # state 4 - processing image finished
                # state 5 - showing image and waiting for restart
                if result is not None and (result['state'] == 1 or result['state'] == 3 or result['state'] == 4):
                    message_json = json.dumps(result)
                    print(f"Sending message for state: {result['state']}")
                    sock.send(message_json)

            time.sleep(0.1)

    except ConnectionClosed as ex:
        print(f"Connection terminated by the client. {ex}")
    except Exception as ex:
        print(f"Unexpected error occurred. {ex}")

    connection_count -= 1
    if connection_count == 0:
        analysis_service.started = False