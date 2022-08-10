import math
import cv2 as cv
import numpy as np
from model.pcb_flow import PCBFlow

class NormalizacaoService():
    
    def normIllumination(self, pcb_flow : PCBFlow, DCTdistance = 10, dataType = "float64", base = 2):

        img = cv.cvtColor(pcb_flow.img_bordas, cv.COLOR_RGB2GRAY)

        # 1. Log transform
        lut = np.asarray([math.log(i, base) for i in (np.arange(0, 256) + 1)], dataType)
        img_log = cv.LUT(img, lut)

        # 2. DCT transform
        DCTCoeficient = cv.dct(img_log)

        # 2.1. Remove DCT coeficients
        if(DCTdistance > 1):
            indices = np.array([[j, i-j] for i in np.arange(1, DCTdistance) for j in np.arange(i+1)])
            DCTCoeficient[indices.T[0], indices.T[1]] = 0

        # 3. IDCT transform
        img_IDCT = cv.idct(DCTCoeficient)

        img_IDCT_2 = img_IDCT.copy()

        # 3.1. Normalizing values between [0, 1]
        imgMax = np.max(img_IDCT)
        imgMin = np.min(img_IDCT)
        img_IDCT -= imgMin
        img_IDCT /= (imgMax-imgMin)

        # Option
        # # 3.1. (b) Inverse log transform
        height = img_IDCT_2.shape[0]
        width = img_IDCT_2.shape[1]
        img_IDCT_linear = np.asarray([(math.pow(base, img_IDCT_2[i,j]) - 1)
                        for i in np.arange(height)
                        for j in np.arange(width)]).reshape(height, width)
        img_IDCT_linear[img_IDCT_linear < 0] = 0
        img_IDCT_linear[img_IDCT_linear > 255] = 255

        img_IDCT_linear_uint8 = (img_IDCT_linear).astype("uint8")

        return img_IDCT_linear_uint8