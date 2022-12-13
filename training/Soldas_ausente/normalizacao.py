import pandas as pd
import cv2 as cv
import numpy as np
import imageio
import os

def carrega_img(lista, x): #Pasta de origem das imagens, lista que as imagens pertecem, numero de imagens
	for i in range(x):
		filename = ("Solda_{}.png".format(i+1))
		lista.append(imageio.imread(filename))
	return lista

def colorN(srcRGB, srcGray):

    h, w = srcGray.shape
    if (h%2 != 0):
        h -= 1
    if (w%2 != 0):
        w -= 1

    dstGray = np.copy(srcGray[:h, :w])
    dstRGB = np.copy(srcRGB[:h, :w, :])

    miu = np.log10(dstGray.mean())
    C_00 = miu*np.sqrt(h*w)
    #print("h = ", h, ", w = ", w, ", miu = ", miu, ", C_00 = ", C_00)

    vis0 = np.zeros((h, w), np.float64)
    vis0 += dstGray
    vis0 += 1.0
    vis0 = np.log10(vis0)
    vis1 = cv.dct(vis0)

    Ddis = 15

    vis2 = np.copy(vis1)
    for i in range(Ddis):
        for j in range(i + 1):
            #vis2[i - j, j] = C_00
            vis2[i - j, j] = 0
    vis2 = cv.idct(vis2)
    #vis2 = np.exp(vis2) - 1
    vis2 = (10.0**vis2) - 1
    #vis2 -= 1
    dstGray = cv.normalize(vis2, None, 0, 255, cv.NORM_MINMAX, dtype=cv.CV_8U)


    for color in range(3):
        vis0 = np.zeros((h, w), np.float64)
        vis0 += dstRGB[:, :, color]
        vis0 += 1.0
        vis0 = np.log10(vis0)
        vis1 = cv.dct(vis0)
        vis2 = np.copy(vis1)
        miu = np.log10(dstRGB[:, :, color].mean())
        C_00 = miu*np.sqrt(h*w)
        #print("h = ", h, ", w = ", w, ", miu = ", miu, ", C_00 = ", C_00)
        for i in range(Ddis):
            for j in range(i + 1):
                #vis2[i - j, j] = C_00
                vis2[i - j, j] = 0
        vis2 = cv.idct(vis2)
        #vis2 = np.exp(vis2) - 1
        vis2 = (10.0**vis2) - 1
        #vis2 -= 1
        vis3 = cv.normalize(vis2, None, 0, 255, cv.NORM_MINMAX, dtype=cv.CV_8U)
        dstRGB[:, :, color] = vis3
        
    #cv.imwrite("DCT.png", dstRGB)
    #cv.imwrite("DCT_gray.png", dstGray)

    return dstRGB


### Listas com as imagens

#images = []

fimg = []
O_soldas = []

carrega_img(O_soldas, 63)

C_soldas = O_soldas.copy()

for i in range(63):
	O_soldas[i] = cv.cvtColor(O_soldas[i], cv.COLOR_BGR2GRAY)
	O_soldas[i] = colorN(C_soldas[i], O_soldas)

for i in range(63):
	cv.imwrite('Solda_%i.png' %i, O_soldas_boas[i])