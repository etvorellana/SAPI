import time, json
from flask import Flask, render_template
from flask_sock import Sock, ConnectionClosed
from controller.analysis_controller import analysis_blueprint

app = Flask(__name__)

# add controllers
app.register_blueprint(analysis_blueprint)

# run server when this file as script
if __name__ == "__main__":
    app.run()
    