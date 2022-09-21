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
        imgMax = np.max(dctImage)
        imgMin = np.min(dctImage)
        dctImage -= imgMin
        dctImage /= (imgMax-imgMin)
        return dctImage

    def operacao_dct(self, img_solda):
        soma = np.sum(img_solda)
        desvio = np.std(img_solda)
        return soma, desvio

    def dctSum(self, img):
        soma_dct, desvio_dct = self.operacao_dct(img)
        lista_valores = []
        lista_valores.append(soma_dct)
        lista_valores.append(desvio_dct)

        return lista_valores
