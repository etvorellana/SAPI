import numpy as np
import pywt

class DwtService():
    def __init__(self):
        pass

    def dwt_filter(self, img):
        (cA, cD) = pywt.dwt(img, 'db1')
        return cA

    def operacao_dwt(self, img_solda):
        soma = np.sum(img_solda)
        media = np.mean(img_solda)
        desvio = np.std(img_solda)
        minValue = np.min(img_solda)
        maxValue = np.max(img_solda)
        return soma, media, desvio, minValue, maxValue

    def dwtSum(self, img):
        soma_dwt, media, desvio_dwt, minValue, maxValue = self.operacao_dwt(img)
        lista_valores = np.zeros(5)
        lista_valores[0] = soma_dwt
        lista_valores[1] = media
        lista_valores[2] = desvio_dwt
        lista_valores[3] = minValue
        lista_valores[4] = maxValue

        return lista_valores
