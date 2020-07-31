
# Importando os módulos
import sys
import argparse
import numpy as np
#import pandas as pd
import matplotlib as math
import matplotlib.pyplot as plt
import cv2 as cv
import imutils
# Versão dos pacotes utilizados
def showVersions():
    print(" Processamento de imagens de PCB")
    print("para analise de soldas.")
    print("Processado com:")
    print("Python:", sys.version)
    print("Argparse: ", argparse.__version__)
    print("NumPy: ", np.__version__)
    #print("Pandas: ", pd.__version__)
    print("Mathplotlib: ", math.__version__)
    print("OprnCV: ", cv.__version__)
    print("Imutils: ", imutils.__version__)

# Carregando imagem de arquivo
def loadImage(fileName, filterType = 0, 
                ksize = 5, gksize = (5,5)):
    ''' Função loadImage carrega uma imagem
        de um arquivo e, eventualmente, pode
        aplicar alguns filtros nela
        Input:
            fileName: Nome do arquivo
            filterType: Tipo de filtro a ser
            utilizado (0:None, 1:medianBlur,
                        2: GaussianBlur)
            ksize: aperture linear size; it 
            must be odd and greater than 1, 
            for example: 3, 5, 7
            gksize - Gaussian kernel size.
            (ksize.width,ksize.height) 
            ksize.width and ksize.height can 
            differ but they both must be 
            positive and odd.

        Output:
            srcGrey: Imagem em tons de cinza
            srcRGB: Imagem em formato RGB
    '''
    srcGrey = cv.imread(fileName, cv.IMREAD_GRAYSCALE)
    srcRGB = cv.imread(fileName)
    # Colocar mais um parametro nesta função para dar opções de filtrar
    if filterType == 1:
        srcGrey = cv.medianBlur(srcGrey, ksize)
    elif filterType == 2:
        srcGrey = cv.GaussianBlur(srcGrey, gksize, 0)

    return srcGrey, srcRGB

def takepic():
    pass

def imagShow(title, img):
    cv.namedWindow(title, cv.WINDOW_NORMAL)
    cv.imshow(title, img)
    #cv.waitKey()

def PCBextract(img, target = 0.5 ,mx= 40, my = 40):
    ''' Função para extrair a PCB da imagem
        Input: 
            img: imagem a ser processada
            mx: tamanho da borda em x
            mx: tamanho da borada em y
        Output: 


    '''
    height, width, col = img.shape

    # transforma imagem rgb em hsv
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # binarização da imagem
    green_lower = (60, 60, 20)
    green_upper = (100, 255, 140)
    mask = cv.inRange(hsv, green_lower, green_upper)

    # contornos
    contours = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    cutArea = target*height*width

    # verificar areas dos contornos e cortar
    if len(contours) > 0:
        for i in range(len(contours)):
            area = cv.contourArea(contours[i])
            if area > cutArea:
                #print(area)
                x, y, w, h = cv.boundingRect(contours[i])
                cut_image = img[y - my:y + h + my, x - mx:x + w + mx, :].copy()
                # desenhar contorno da placa
                contour = cv.drawContours(np.zeros_like(img), contours, i, (255,255,255), 3)
                contour = contour[y - my:y + h + my, x - mx:x + w + mx, :].copy()
                break

    return contour, cut_image

def main(argv):
    showVersions()
    ##  Recebimento dos argumentos
    parser = argparse.ArgumentParser(description = 'Detecção de solda')
    parser.add_argument('--arquivo', action = 'store', 
                        dest = 'src', default = 'capt', 
                        required = False, help = 'Nome do arquivo de imagem ou "capt" para utilizar a camera')
    # parser.add_argument('-filtro', type = int, action = 'store', 
    #                     dest = 'filtro', default = 1, required = False, 
    #                     help = 'Tipo se filtro a ser aplicado: 1- Sem Filtro; 2 - Median Blur; 3 - Gaussian Blur ')
    # parser.add_argument('-borda', type = int, action = 'store', 
    #                     dest = 'borda', default = 1, required = False, 
    #                     help = 'Tipo de detecção de borda a ser aplicado: 1- Corner Harris 2 - Hough Lines')
    

    arguments = parser.parse_args()

    # In-01: Input
    ##  Verifica se carrega o arquivo ou tira uma foto
    if (arguments.src == 'capt'):
        srcGrey, srcRGB = takepic() #   Chama função da camera
    else:
        srcGrey, srcRGB = loadImage(arguments.src) # Carrega Imagem

    
    # Out-01: Input
    print("Tamanho imagem 03 Original: ", srcRGB.shape)
    imagShow("Original Grey", srcGrey)
    imagShow("Original RGB", srcRGB)
    cv.waitKey()

    # In-02: Macro Segmentation
    contour, srcRGB = PCBextract(srcRGB.copy())
    srcGrey = cv.cvtColor(srcRGB, cv.COLOR_BGR2GRAY)
    # Out-02
    print("Tamanho imagem segmentada: ", srcRGB.shape)
    imagShow("Macro Segmentation Grey", srcGrey)
    imagShow("Macro Segmentation RGB", srcRGB)
    imagShow("Macro Segmentation Contour", contour)
    cv.waitKey()

    



    

if __name__ == "__main__":
    main(sys.argv[1:])