import sys
import argparse
import math
import cv2 as cv
import numpy as np
import skimage
#from skimage.color import rgb2yiq
import time
#import picamera

##############################  CORREÇÕES A SEREM FEITAS    ##############################
######  * Correção da normalização de cores, coreção do DCT
######  * Correção do skimage para conversão YIQ
######  * Correção do erro de overflow na busca do limiar de algumas imagens


######  Bloco Inicial

##   Carrega Imagem
def loadImage(fileName):
    
    srcGray = cv.imread(cv.samples.findFile(fileName), cv.IMREAD_GRAYSCALE) #   Carrega em escala de cinza
    srcRGB = cv.imread(cv.samples.findFile(fileName)) # Carrega a imagem colorida

    return srcGray, srcRGB

##   Tira uma fotografia utilizando picamera (testar no rasp) e coloca em um numpy
def takepic():

    with picamera.PiCamera() as camera:
        camera.resolution = (2592, 1944) #  Define a resolução da camera
        camera.framerate = 24
        time.sleep(2)
        srcRGB = np.empty((2592 * 1944 * 3,), dtype=np.uint8)
        camera.capture(srcRGB, 'bgr')
        srcRGB = srcRGB.reshape((2592, 1944, 3))
        srcGray = cv.cvtColor(srcRGB, cv.COLOR_BGR2GRAY)
        
    return srcGray, srcRGB

##  Aplica filtro na Imagem
def filter(srcGray, opt):

    if opt == 2:
        srcGray = cv.medianBlur(srcGray, 11) #  Aplica filtro Median Blur
    elif opt == 3:
        srcGray = cv.GaussianBlur(srcGray, (5, 5), 0) # Aplica filtro Gaussian Blur

    return srcGray

#####   Bloco de detecção de bordas

## Detecção de cantos e correção de pespectiva com corner Harris
def CornerPespec(srcRGB):
    ##  Blur para suavizar e evitar ruidos
    dst = cv.blur(srcRGB,(5,5))

    ##  Canny
    dst = cv.Canny(dst, 50, 100, None, 3, True)

    dst = np.float32(dst)

    ##  Detectar as quinas
    dst = cv.cornerHarris(dst,2,3,0.04)

##    cv.namedWindow('Corner',cv.WINDOW_NORMAL)
##    cv.imshow('Corner', dst)

    ##  Dilatação para destacar
    dst = cv.dilate(dst,None)

    N, M = dst.shape

    ##  Superior Esquerdo
    lt = (0,0)
    plt = (0,0)
    dlt = N**2+M**2

    ##  Superior Direito
    rt = (0,M)
    prt = (0,M)
    drt = N**2+M**2

    ##  Inferior Direito
    rb = (N,M)
    prb = (N,M)
    drb = N**2+M**2

    ##  Inferior Esquerdo
    lb = (N,0)
    plb = (N,0)
    dlb = N**2+M**2

    ##  Calcular Distancia entre os pontos
    for i in range (0, N):
        for j in range (0, M):
            if (dst[i][j] != 0):
                ##  LT
                if (i < (N/2)) and (j < (M/2)):
                     dltc = ((i-lt[0])**2)+((j-lt[1])**2)
                     if (dltc < dlt):
                         plt = (i,j)
                         dlt = dltc
                ##  RT
                if (i < (N/2)) and (j > (M/2)):
                     drtc = ((i-rt[0])**2)+((rt[1]-j)**2)
                     if drtc < drt:
                         prt = (i,j)
                         drt = drtc
                ##  RB
                if (i > (N/2)) and (j > (M/2)):
                     drbc = ((rb[0]-i)**2)+((rb[1]-j)**2)
                     if drbc < drb:
                         prb = (i,j)
                         drb = drbc
                ##  LB
                if (i > (N/2)) and (j < (M/2)):
                     dlbc = ((lb[0]-i)**2)+((j-lb[1])**2)
                     if dlbc < dlb:
                         plb = (i,j)
                         dlb = dlbc
                
                
##    print("coodernadas Superior Esquerda:", plt)
##    print("coodernadas Superior Direita:", prt)
##    print("coodernadas Inferior Direita:", prb)
##    print("coodernadas Inferior Esquerda:", plb)

    ##  Pontos para calcular delta
    if plt[0] < prt[0]:
        nt = plt[0]
    else:
        nt = prt[0]
    if plb[0] > prb[0]:
        nb = plb[0]
    else:
        nb = prb[0]

    if plt[1] < plb[1]:
        ml = plt[1]
    else:
        ml = plb[1]
        
    if prt[1] > prb[1]:
        mr = prt[1]
    else:
        mr = prb[1]

    ##  DeltaN e DeltaM
    dn = nb - nt
    dm = mr - ml

##    print ("nt:", nt)
##    print ("nb:", nb)
##    print ("ml:", ml)
##    print ("mr:", mr)
##    print ("dN:", dn)
##    print ("dM:", dm)

    ##  Corrigir a pespectiva
    pts1 = np.float32([[plt[1],plt[0]], [prt[1],prt[0]], [plb[1],plb[0]], [prb[1],prb[0]]])
    pts2 = np.float32([[0,0],[dm,0],[0,dn],[dm,dn]])

    matrix = cv.getPerspectiveTransform(pts1, pts2)
    result = cv.warpPerspective(img, matrix, (dm, dn))
    resultGray = cv.cvtColor(result,cv.COLOR_BGR2GRAY)

##    cv.circle(srcRGB,(plt[1],plt[0]), 10, (0,0,255), -1)
##    cv.circle(srcRGB,(plb[1],plb[0]), 10, (0,255,0), -1)
##    cv.circle(srcRGB,(prt[1],prt[0]), 10, (255,0,0), -1)
##    cv.circle(srcRGB,(prb[1],prb[0]), 10, (0,255,255), -1)
##
##    cv.namedWindow('Cantos',cv.WINDOW_NORMAL)
##    cv.imshow('Cantos', srcRGB)
##
##    cv.namedWindow('dst',cv.WINDOW_NORMAL)
##    cv.imshow('dst',result)
##
##    cv.imwrite("Foto_seg.png", result)

    return result, resultGray

def edgesDetection(src, thr1=50, thr2=100, apSize=3, L2Grad=True):

    #   Função Canny(image, threshold1, threshold2[, edges[, apertureSize[, L2gradient]]]) -> edges
    dst = cv.Canny(src, thr1, thr2, None, apSize, L2Grad)
    return dst


def borderPCB(src, rho=1, theta=np.pi / 180, thr=50, minLLght=50, maxLGap=10):

    #   Função HoughLinesP(image, rho, theta, threshold[, lines[, minLineLength[, maxLineGap]]]) -> lines
    #   Implementação da função probabilistica da Transformada de Hough para detecção de linhas
    linesP = cv.HoughLinesP(src, rho, theta, thr, None, minLLght, maxLGap)
    (x1, y1, x2, y2) = (0, 0, 0, 0)
    if linesP is not None:
        N, M = src.shape
        r_min = N ** 2 + M ** 2
        # Determinando mais próxima da origem
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            r = l[0] ** 2 + l[1] ** 2
            if r < r_min:
                (x1, y1, x2, y2) = (l[0], l[1], l[2], l[3])
                r_min = r

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        if dx > dy:  # se ela for maior na direção x esticamos em x
            for x in range(x2 + 1, M):
                if src[y2, x] > 0:  # procuramos primeiro a direita
                    x2 = x
                elif src[y2 - 1, x] > 0:  # depois procuramos acima
                    x2 = x
                    y2 = y2 - 1
                elif src[y2 + 1, x] > 0:  # depois procuramos abaixo
                    x2 = x
                    y2 = y2 + 1
                else:  # se não tiver mais pontos da reta paramos
                    break
        else:  # se ela for maior na direção y esticamos em y
            for y in range(y2 + 1, N // 2):  #
                if src[y, x2] > 0:  # procuramos primeiro abaixo
                    y2 = y
                elif src[y, x2 + 1] > 0:  # depois procuramos a izquerda
                    y2 = y
                    x2 = x2 + 1
                elif src[y, x2 - 1] > 0:  # depois procuramos a direita
                    y2 = y
                    x2 = x2 - 1
                else:  # se não tiver mais pontos da reta paramos
                    break
    return x1, y1, x2, y2


#####   BLOCO PARA ALINHAMENTO

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

#####   BLOCO PARA NORMALIZAÇÂO DE CORES
def colorN(srcRGB, N=5):
    h, w, d = srcRGB.shape
    #print(h, w, d)
    dstRGB = np.copy(srcRGB)
    for i in range(d):
        miu = np.log10(srcRGB[:, :, i].mean())
        C_00 = miu * math.sqrt(h * w)
        # C_00 = 0
        vis0 = np.zeros((h, w), np.float32)
        vis3 = np.zeros((h, w), np.float32)
        vis0[:h, :w] = srcRGB[:h, :w, i]
        vis0 += 1
        c = 255 / np.log10(vis0.max())
        #print(c)
        vis0 = c * np.log10(vis0)
        # vis0_1 = cv.normalize(vis0, None, 0, 255, cv.NORM_MINMAX, dtype=cv.CV_8U)
        # cv.imshow("Log", vis0_1)
        vis1 = cv.dct(vis0)
        # cv.imshow("DCT", vis1)
        for k in range(N):
            for j in range(i + 1):
                vis1[k - j, j] = C_00
        # cv.imshow("DCT Normalize", vis1)

        vis2 = cv.idct(vis1)
        # vis2 = cv.normalize(vis2, None, 0, 255, cv.NORM_MINMAX, dtype=cv.CV_8U)
        # cv.imshow("iDCT", vis2)
        vis3 = (1.02 ** vis2) - 1
        vis3 = cv.normalize(vis3, None, 0, 255, cv.NORM_MINMAX, dtype=cv.CV_8U)
        dstRGB[:h, :w, i] = vis3[:h, :w]
    # cv.imshow("iLog", vis3)
    return dstRGB

#####   BLOCO ONDE É REALIZADA A CONVERSÃO PARA YIQ, THRESHOLD E BINARIZAÇÃO
def threshold(src, dst):

    cutYIQ = skimage.color.rgb2yiq(src) #   Utilizando o pacote skimage é realizada a transformação para o espaço de cor YIQ
    thrGrey = np.zeros_like(dst) 
    Y_min = cutYIQ[:, :, 0].min() # Menor pixel com cor
    Y_max = cutYIQ[:, :, 0].max() # Maior pixel com cor
    Y_med = (Y_max + Y_min) / 2 #   Media das cores
    cont = 0
    con_L0 = 0
    con_H0 = 0
    con_L1 = 1
    con_H1 = 0
    M, N, d = cutYIQ.shape
    #   Busca pelo limiar da imagem
    while (con_L0 != con_L1) and cont < 100:
        cont += 1
        #(cont, con_L1, con_H1, Y_med)
        sum_L = 0
        sum_H = 0
        con_L0 = con_L1
        con_H0 = con_H1
        con_H1 = 0
        con_L1 = 0

        for i in range(M):
            for j in range(N):
                if cutYIQ[i, j, 0] < Y_med:
                    sum_L += cutYIQ[i, j, 0]
                    con_L1 += 1
                else:
                    sum_H += cutYIQ[i, j, 0]
                    con_H1 += 1

        Y_min = sum_L / con_L1
        Y_max = sum_H / con_H1
        Y_med = (Y_max + Y_min) / 2.0
    #   Após encontrar o limiar binariza a imagem, tudo que for maior que o limiar fica branco e o que for menor preto
    for i in range(M):
        for j in range(N):
            if cutYIQ[i, j, 0] >= Y_med:
                thrGrey[i, j] = 255
    return thrGrey #    Retorna a imagem binarizada

#####   BLOCO PARA SEGMENTAÇÂO
def segment_01(thrGrey, normRGB):

    #   Copia a imagem com o limiar
    im_floodfill = thrGrey.copy()
    img = normRGB.copy()

    #   Cria uma mascara usando a funação floodfill
    #   O tamanho precisa ser 2 pixels a mais que a imagem
    h, w = thrGrey.shape[:2]
    (x_0, y_0) = (0, 0)
    mask = np.zeros((h + 2, w + 2), np.uint8)
    if h < w:
        s = h - 1
    else:
        s = w - 1
    for i in range(1, s):
        if im_floodfill[i - 1 : i + 2, i - 1 : i + 2].sum() == 0:
            # print("Ok")
            (x_0, y_0) = (i, i)
            break

    #   Preenchimento dos pontos (x_0, y_0)
    cv.floodFill(im_floodfill, mask, (x_0, y_0), 255)
    '''
    cv.namedWindow("Floodfilled Image", cv.WINDOW_NORMAL)
    cv.imshow("Floodfilled Image", im_floodfill)
    '''

    #   Inverte a Imagem do floodfill
    im_floodfill_inv = cv.bitwise_not(im_floodfill)
    '''
    cv.namedWindow("Inverted Floodfilled Image", cv.WINDOW_NORMAL)
    cv.imshow("Inverted Floodfilled Image", im_floodfill_inv)
    '''

    #   Combine as duas imagens para obter a areas de interesse
    im_out = thrGrey | im_floodfill_inv
    '''
    cv.namedWindow("Combined Floodfilled Image", cv.WINDOW_NORMAL)
    cv.imshow("Combined Floodfilled Image", im_out)
    '''

    #   Encontro os contornos
    contours, hierarchy = cv.findContours(im_out, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # print("hierarchy: ", hierarchy.shape)
    # print("contours: ", len(contours))
    sections = []
    for c in contours:
        M = cv.moments(c)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            x, y, w, h = cv.boundingRect(c)
            if (abs(w - h) < 25) and ((w * h) < 600) and ((w * h) > 200):
                sections.append((cX, cY, x, y, w, h))
                # cv.circle(img, (cX, cY), 2, (255, 255, 255), -1)
                cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)

    # print("sections: ", len(sections))
    # externs = []
    # for i in range(len(sections)):
    #     (AcX, AcY, Ax, Ay, Aw, Ah) = sections[i]
    #     for j in range(len(sections)):
    #         if i != j:
    #             (BcX, BcY, Bx, By, Bw, Bh) = sections[j]
    #             # print(j, " - B: ", sections[j])
    #             if (
    #                 (BcX > Ax)
    #                 and (BcX < (Ax + Aw))
    #                 and (BcY > Ay)
    #                 and (BcY < (Ay + Ah))
    #             ):
    #                 externs.append((AcX, AcY, Ax, Ay, Aw, Ah))
    #                 break
    #
    # print("externs: ", len(externs))
    # for c in externs:
    #     (AcX, AcY, Ax, Ay, Aw, Ah) = c
    #     cv.circle(img, (AcX, AcY), 2, (255, 255, 255), -1)
    #     cv.rectangle(img, (Ax, Ay), (Ax + Aw, Ay + Ah), (0, 0, 255), 2)
    '''
    cv.namedWindow("Segmented Image", cv.WINDOW_NORMAL)
    cv.imshow("Segmented Image", img)
    print("contours: ", len(sections))
    '''
    return sections


def main(argv):

    
    ##  Recebimento dos argumentos
    parser = argparse.ArgumentParser(description = 'Detecção de solda')
    parser.add_argument('--arquivo', action = 'store', dest = 'src', default = 'foto', required = False, help = 'Nome do arquivo de imagem ou "foto" para utilizar a camera')
    parser.add_argument('-filtro', type = int, action = 'store', dest = 'filtro', default = 1, required = False, help = 'Tipo se filtro a ser aplicado: 1- Sem Filtro; 2 - Median Blur; 3 - Gaussian Blur ')
    parser.add_argument('-borda', type = int, action = 'store', dest = 'borda', default = 1, required = False, help = 'Tipo de detecção de borda a ser aplicado: 1- Corner Harris 2 - Hough Lines')
    
    arguments = parser.parse_args()

    ##  Verifica se carrega o arquivo ou tira uma foto
    if (arguments.src == 'foto'):
        srcGrey, srcRGB = takepic() #   Chama função da camera
    else:
        srcGrey, srcRGB = loadImage(arguments.src) # Carrega Imagem
    '''
    cv.namedWindow("Original Grey", cv.WINDOW_NORMAL)
    cv.imshow("Original Grey", srcGrey)
    cv.namedWindow("Original RGB", cv.WINDOW_NORMAL)
    cv.imshow("Original RGB", srcRGB)
    '''
    
    ## Aplica o filtro na imagem, caso tenha sido escohido
    if (arguments.filtro == 2) or (arguments.filtro == 3):
        srcGrey = filter(srcGrey, arguments.filtro)
        '''
        cv.namedWindow("Filter", cv.WINDOW_NORMAL)
        cv.imshow("Filter", srcGrey)
        '''

    ##  Decção de bordas
    if (arguments.borda == 1):
        srcRGB, srcGrey = CornerPespec(srcRGB)
    else:
        edges = edgesDetection(srcGrey)
        '''
        cv.namedWindow("Canny Output", cv.WINDOW_NORMAL)
        cv.imshow("Canny Output", edges)
        '''
        #   Detecta a maior borda
        border = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)
        x1, y1, x2, y2 = borderPCB(edges)
        cv.line(border, (x1, y1), (x2, y2), (0, 0, 255), 1, cv.LINE_AA) #   Desenha linha na bordas
        '''
        cv.namedWindow("PCB border", cv.WINDOW_NORMAL)
        cv.imshow("PCB border", border)
        '''
        #   Alinhamento
        aliGrey = alignment(srcGrey, x1, y1, x2, y2)
        aliRGB = alignment(srcRGB, x1, y1, x2, y2)
        '''
        cv.namedWindow("Alignment Grey", cv.WINDOW_NORMAL)
        cv.imshow("Alignment Grey", aliGrey)
        cv.namedWindow("Alignment RGB", cv.WINDOW_NORMAL)
        cv.imshow("Alignment RGB", aliRGB)
        '''
        #   Corta região da placa
        cutGrey = aliGrey[y1:, x1:] 
        cutRGB = aliRGB[y1:, x1:]
        cutGrey = srcGrey
        cutRGB = srcRGB
        '''
        cv.namedWindow("Grey - cut and aligned", cv.WINDOW_NORMAL)
        cv.imshow("Grey - cut and aligned", cutGrey)
        cv.namedWindow("RGB - cut and aligned", cv.WINDOW_NORMAL)
        cv.imshow("RGB - cut and aligned", cutRGB)
        '''
        
    #   Normalização de cor
    # print(cutRGB[:, :, 0].shape)
    normRGB = colorN(srcRGB, 5)
    '''
    cv.namedWindow("Normalize - RGB", cv.WINDOW_NORMAL)
    cv.imshow("Normalize - RGB", normRGB)
    '''
    # Thresholding
    thrGrey = threshold(normRGB, srcGrey)
    #thrGrey = threshold(srcRGB, srcGrey)
    '''
    cv.namedWindow("YIQ - Thresold", cv.WINDOW_NORMAL)
    cv.imshow("YIQ - Thresold", thrGrey)
    '''
    segList = segment_01(thrGrey, normRGB)
    cv.waitKey()
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
