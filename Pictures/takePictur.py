from gpiozero import Button
from picamera import PiCamera
from datetime import datetime
from signal import pause
 

clikButton = Button(6)

camera = PiCamera()

def capture():
    timestamp = datetime.now().isoformat()
    camera.capture('/home/pi/Pictures/%s.png' % timestamp)

clikButton.when_pressed = capture

pause()
