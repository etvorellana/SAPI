import base64
from io import BytesIO
import numpy as np
import cv2 as cv
from PIL import Image
import time
# import picamera

def loadImage(fileName):
    srcRGB = cv.imread(cv.samples.findFile(fileName)) # Carrega a imagem colorida
    return srcRGB

##   Tira uma fotografia utilizando picamera (testar no rasp) e coloca em um numpy
def takepic():

    with picamera.PiCamera() as camera:
        camera.resolution = (2592, 1944) #  Define a resolução da camera
        camera.framerate = 24
        time.sleep(2)
        srcRGB = np.empty((2592 * 1944 * 3,), dtype=np.uint8)
        camera.capture(srcRGB, 'bgr')
        srcRGB = srcRGB.reshape((2592, 1944, 3))
        srcGray = cv.cvtColor(srcRGB, cv.COLOR_BGR2GRAY)
        
    return srcGray, srcRGB

##  Aplica filtro na Imagem
def filter(srcGray, opt):

    if opt == 2:
        srcGray = cv.medianBlur(srcGray, 11) #  Aplica filtro Median Blur
    elif opt == 3:
        srcGray = cv.GaussianBlur(srcGray, (5, 5), 0) # Aplica filtro Gaussian Blur

    return srcGray

def from_np_array_to_base64(image, format = "png"):
    pil_img = Image.fromarray(image)
    buff = BytesIO()
    pil_img.save(buff, format)
    encoded_image = base64.b64encode(buff.getvalue())

    return encoded_image.decode()