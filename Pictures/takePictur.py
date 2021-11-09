import os
from dotenv import load_dotenv, find_dotenv
from gpiozero import Button
from picamera import PiCamera
from datetime import datetime
from signal import pause

load_dotenv(find_dotenv())

clikButton = Button(6)

camera = PiCamera()

def capture():
    timestamp = datetime.now().isoformat()
    # camera.capture('/home/pi/Pictures/%s.png' % timestamp)
    camera.capture('%s%s.png' % (os.getenv("DEFAULT_PATH"), timestamp))

clikButton.when_pressed = capture

pause()
