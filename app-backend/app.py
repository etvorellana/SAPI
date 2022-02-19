from flask import Flask, render_template
from controller.analysis_controller import analysis_blueprint
from controller.button_controller import button_blueprint
from controller.camera_controller import camera_blueprint

app = Flask(__name__)

# add controllers
app.register_blueprint(analysis_blueprint, url_prefix = "/analysis")
app.register_blueprint(button_blueprint, url_prefix = "/button")
app.register_blueprint(camera_blueprint, url_prefix = "/camera")

@app.route('/')
def index():
    return render_template('index.html')

# run server when this file is executed as script
if __name__ == "__main__":
    app.run()
    