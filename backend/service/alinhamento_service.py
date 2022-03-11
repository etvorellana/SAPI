from model.pcb_flow import PCBFlow
import numpy as np
import cv2 as cv
import math

class AlinhamentoService():
    def alignment(src, x1, y1, x2, y2):
        # Pega as dimensões da imagem
        shape = src.shape
        N = shape[0]
        M = shape[1]
        dx = x2 - x1
        dy = y2 - y1
        #   Descobre a inclinação da Imagem e calcula o angulo theta para fazer a rotação
        if dx > dy:
            theta = np.rad2deg(math.atan(dy / dx))
        else:
            theta = np.rad2deg(math.atan(-dx / dy))

        # Cria a matrix de rotação
        rotMat = cv.getRotationMatrix2D((x1, y1), theta, 1)
        rot = cv.warpAffine(src, rotMat, (M, N)) #  Rotaciona a imagem com a função warpAffine
        return rot

    def getOptimalDCTSize(N): 
        return 2*cv.getOptimalDFTSize((N+1)//2)