import math
import cv2 as cv
import numpy as np

class DctService():
    def __init__(self):
        pass

    def dct_filter(self, img):
        gray_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        lut = np.asarray([math.log(i, 2) for i in (np.arange(0, 256) + 1)], "float64")
        img_log = cv.LUT(gray_img, lut)
        dctImage = cv.dct(img_log)
        return dctImage

    def operacao_dct(self, img_solda):
        soma = np.sum(img_solda)
        media = np.mean(img_solda)
        desvio = np.std(img_solda)
        minValue = np.min(img_solda)
        maxValue = np.max(img_solda)
        return soma, media, desvio, minValue, maxValue
        #return desvio, minValue

    def dctSum(self, img):
        soma_dct, media, desvio_dct, minValue, maxValue = self.operacao_dct(img)
        #desvio_dct, minValue = self.operacao_dct(img)
        lista_valores = np.zeros(5)
        #lista_valores = np.zeros(2)
        lista_valores[0] = soma_dct
        lista_valores[1] = media
        lista_valores[2] = desvio_dct
        lista_valores[3] = minValue
        lista_valores[4] = maxValue

        return lista_valores
