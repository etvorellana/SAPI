from gpiozero import Button
import os
from signal import pause
    
def shutdown():
    os.system("sudo shutdown now -h")

stopButton = Button(2)

stopButton.when_pressed = shutdown

pause()