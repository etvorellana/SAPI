!#/bin/bash
source ./rpi-cam-prototype-env/bin/activate
cd app-backend/Pictures
python shutdown.py
deactivate
