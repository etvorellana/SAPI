from model.pcb_flow import PCBFlow
import numpy as np
from skimage.color import rgb2yiq

class ThresholdService():
    def tratar(self, pcb_flow : PCBFlow):
        return self.threshold(pcb_flow.img_norm)
    
    def threshold(self, dstRGB):
        cutYIQ = rgb2yiq(dstRGB)
        #thrGray = np.zeros_like(dstGray)
        Y_min = cutYIQ[:, :, 0].min() # Menor pixel com cor
        Y_max = cutYIQ[:, :, 0].max() # Maior pixel com cor
        Y_med = (Y_max + Y_min) / 2 #   Media das cores
        cont = 0
        con_L0 = 0
        con_L1 = 1
        N, M, d = cutYIQ.shape
        a = cutYIQ[:, :, 0]
        quantT = N*M
        while ((con_L0 != con_L1) and (cont < 100)):
            cont += 1
            con_L0 = con_L1
            b = np.where(a < Y_med, a, 0)
            soma = b.sum()
            quant = np.count_nonzero(b)
            con_L1 = quant
            Y_min = soma/quant
            soma = a.sum() - soma;
            quant = quantT - quant
            #print(soma, quant, soma/quant)
            Y_max = soma/quant
            Y_med = (Y_max + Y_min) / 2.0

        print(cont)
        thrGray = np.where(a < Y_med, 0, 255)
        #thrGray = cv.normalize(thrGray, None, 0, 255, cv.NORM_MINMAX, dtype=cv.CV_8U)
        thrGray = np.array(thrGray, dtype=np.uint8)
        #print(thrGray.shape)
        return thrGray #    Retorna a imagem binarizada