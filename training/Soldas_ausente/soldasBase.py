import numpy as np
import cv2 as cv
import random


def rotaImagem(imagem, cont = 1):
    nome = "Solda_"
    altura, largura = imagem.shape[:2]
    ponto = (largura / 2, altura / 2) #ponto no centro da figura
    flipImage = cv.flip(imagem, 0)
    cont += 1
    nameFile = nome + str(cont) + ".png"
    print(nameFile)
    cv.imwrite(nameFile, flipImage)
    flipImage = cv.flip(imagem, 1)
    cont += 1
    nameFile = nome + str(cont) + ".png"
    print(nameFile)
    cv.imwrite(nameFile, flipImage)
    flipImage = cv.flip(imagem, -1)
    cont += 1
    nameFile = nome + str(cont) + ".png"
    print(nameFile)
    cv.imwrite(nameFile, flipImage)
    rotaçoes = [30, 45, 60, 120, 135, 150, 210, 225, 240, 300, 315, 330]
    for ang in rotaçoes:
        print(ang)
        rotacao = cv.getRotationMatrix2D(ponto, ang, 1.0)
        rotImg = cv.warpAffine(imagem, rotacao, (largura, altura),
                                flags= cv.INTER_CUBIC,
                                borderMode=cv.BORDER_REPLICATE)
        cont += 1
        nameFile = nome + str(cont) + ".png"
        print(nameFile)
        cv.imwrite(nameFile, rotImg)
    return cont


def main():
    imagem = cv.imread("solda_ausente.png")
    print (imagem.shape)
    altura, largura = imagem.shape[:2]
    # Gravando a imagem original
    nome = "Solda_"
    cv.imwrite("Solda_1.png", imagem)
    #Criando um conjunto de imagens por rotaçao e espelhamento
    cont = 1
    cont = rotaImagem(imagem, cont)
    transla = np.float32([[1, 0, 8],[0, 1, 0]])
    traImg = cv.warpAffine(imagem, transla, (largura, altura),
                        flags= cv.INTER_CUBIC,
                        borderMode=cv.BORDER_WRAP)
    cont += 1
    nameFile = nome + str(cont) + ".png"
    print(nameFile)
    cv.imwrite(nameFile, traImg)
    cont = rotaImagem(traImg, cont)
    transla = np.float32([[1, 0, -8],[0, 1, 0]])
    traImg = cv.warpAffine(imagem, transla, (largura, altura),
                        flags= cv.INTER_CUBIC,
                        borderMode=cv.BORDER_WRAP)
    cont += 1
    nameFile = nome + str(cont) + ".png"
    print(nameFile)
    cv.imwrite(nameFile, traImg)
    cont = rotaImagem(traImg, cont)
    transla = np.float32([[1, 0, 0],[0, 1, 8]])
    traImg = cv.warpAffine(imagem, transla, (largura, altura),
                        flags= cv.INTER_CUBIC,
                        borderMode=cv.BORDER_WRAP)
    cont += 1
    nameFile = nome + str(cont) + ".png"
    print(nameFile)
    cv.imwrite(nameFile, traImg)
    cont = rotaImagem(traImg, cont)
    transla = np.float32([[1, 0, 0],[0, 1, -8]])
    traImg = cv.warpAffine(imagem, transla, (largura, altura),
                        flags= cv.INTER_CUBIC,
                        borderMode=cv.BORDER_WRAP)
    cont += 1
    nameFile = nome + str(cont) + ".png"
    print(nameFile)
    cv.imwrite(nameFile, traImg)
    cont = rotaImagem(traImg, cont)
    transla = np.float32([[1, 0, 8],[0, 1, 8]])
    traImg = cv.warpAffine(imagem, transla, (largura, altura),
                        flags= cv.INTER_CUBIC,
                        borderMode=cv.BORDER_WRAP)
    cont += 1
    nameFile = nome + str(cont) + ".png"
    print(nameFile)
    cv.imwrite(nameFile, traImg)
    cont = rotaImagem(traImg, cont)
    transla = np.float32([[1, 0, -8],[0, 1, 8]])
    traImg = cv.warpAffine(imagem, transla, (largura, altura),
                        flags= cv.INTER_CUBIC,
                        borderMode=cv.BORDER_WRAP)
    cont += 1
    nameFile = nome + str(cont) + ".png"
    print(nameFile)
    cv.imwrite(nameFile, traImg)
    cont = rotaImagem(traImg, cont)
    transla = np.float32([[1, 0, 8],[0, 1, -8]])
    traImg = cv.warpAffine(imagem, transla, (largura, altura),
                        flags= cv.INTER_CUBIC,
                        borderMode=cv.BORDER_WRAP)
    cont += 1
    nameFile = nome + str(cont) + ".png"
    print(nameFile)
    cv.imwrite(nameFile, traImg)
    cont = rotaImagem(traImg, cont)
    transla = np.float32([[1, 0, -8],[0, 1, -8]])
    traImg = cv.warpAffine(imagem, transla, (largura, altura),
                        flags= cv.INTER_CUBIC,
                        borderMode=cv.BORDER_WRAP)
    cont += 1
    nameFile = nome + str(cont) + ".png"
    print(nameFile)
    cv.imwrite(nameFile, traImg)
    cont = rotaImagem(traImg, cont)

if __name__ == "__main__":
    main()
