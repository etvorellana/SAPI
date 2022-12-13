import numpy as np
import cv2

imagem = cv2.imread("Solda_1.png")
print (imagem.shape)
altura, largura = imagem.shape[:2]
ponto = (largura / 2, altura / 2) #ponto no centro da figura

#img_median = cv2.medianBlur(inv, 3) # Add median filter to image
#cv2.imwrite("Solda_1_inver_Suave.png", img_median)

#rotacao 90
rotacao = cv2.getRotationMatrix2D(ponto, 90, 1.0)
rot45 = cv2.warpAffine(imagem, rotacao, (largura, altura))
cv2.imwrite("Solda_2.png", rot45)

#rotacao 180
rotacao = cv2.getRotationMatrix2D(ponto, 180, 1.0)
rot30 = cv2.warpAffine(imagem, rotacao, (largura, altura))
cv2.imwrite("Solda_3.png", rot30)

#rotacao 270
rotacao = cv2.getRotationMatrix2D(ponto, 270, 1.0)
rot60 = cv2.warpAffine(imagem, rotacao, (largura, altura))
cv2.imwrite("Solda_4.png", rot60)

#rotacao 30
rotacao = cv2.getRotationMatrix2D(ponto, 30, 1.0)
rot30 = cv2.warpAffine(imagem, rotacao, (largura, altura))
cv2.imwrite("Solda_5.png", rot30)

#rotacao 45
rotacao = cv2.getRotationMatrix2D(ponto, 45, 1.0)
rot45 = cv2.warpAffine(imagem, rotacao, (largura, altura))
cv2.imwrite("Solda_6.png", rot45)

#rotacao 60
rotacao = cv2.getRotationMatrix2D(ponto, 60, 1.0)
rot60 = cv2.warpAffine(imagem,, rotacao, (largura, altura))
cv2.imwrite("Solda_7.png", rot60)