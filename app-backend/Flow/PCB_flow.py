import sys
import argparse
import math
import cv2 as cv
import numpy as np
#import skimage
from skimage.color import rgb2yiq
import time
#import picamera


######  Bloco Inicial

##   Carrega Imagem
def loadImage(fileName):
    srcRGB = cv.imread(cv.samples.findFile(fileName)) # Carrega a imagem colorida
    return srcRGB

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
    
    h, w, c = srcRGB.shape
    kernel = np.ones((5,5),np.float32)/25

    
    vert = cv.filter2D(srcRGB[:, w//2 -5:w//2 + 5, 1].copy(),-1,kernel)
    vert = vert[:,5]
    
    dvert = np.zeros_like(vert, dtype=np.int16)
    dvert[:] = vert[:]
    dvert[1:-1] = np.abs(dvert[2:] - dvert[:-2])//2

    limits = np.nonzero(dvert[10:-10] > 2.5)
    top = limits[0][0] 
    bot = limits[0][-1] + 20
    
    lt = cv.filter2D(srcRGB[top-100:top+100, :200, :].copy(),-1,kernel)
    lb = cv.filter2D(srcRGB[bot-100:bot+100, :200, :].copy(),-1,kernel)
    
    rt = cv.filter2D(srcRGB[top-100:top+100, w-200:, :].copy(),-1,kernel)
    rb = cv.filter2D(srcRGB[bot-100:bot+100, w-200:, :].copy(),-1,kernel)
    
    #LT
    ##  Canny
    lt = cv.Canny(lt, 50, 100, None, 3, True)
    lt = np.float32(lt)
    ##  Detectar as quinas
    lt = cv.cornerHarris(lt,2,3,0.04)
    ##  Dilatação para destacar
    lt = cv.dilate(lt,None)
    N, M = lt.shape
    plt = (0,0)
    dlt = N**2+M**2
    
    #RT
    ##  Canny
    rt = cv.Canny(rt, 50, 100, None, 3, True)
    rt = np.float32(rt)
    ##  Detectar as quinas
    rt = cv.cornerHarris(rt,2,3,0.04)
    ##  Dilatação para destacar
    rt = cv.dilate(rt,None)
    prt = (0,M)
    drt = dlt
    
    #RB
    ##  Canny
    rb = cv.Canny(rb, 50, 100, None, 3, True)
    rb = np.float32(rb)
    ##  Detectar as quinas
    rb = cv.cornerHarris(rb,2,3,0.04)
    ##  Dilatação para destacar
    rb = cv.dilate(rb,None)
    prb = (N,M)
    drb = dlt
    
    #LB
    ##  Canny
    lb = cv.Canny(lb, 50, 100, None, 3, True)
    lb = np.float32(lb)
    ##  Detectar as quinas
    lb = cv.cornerHarris(lb,2,3,0.04)
    ##  Dilatação para destacar
    lb = cv.dilate(lb,None)
    plb = (N,0)
    dlb = dlt
    
    ##  Calcular Distancia entre os pontos
    for i in range (0, N):
        for j in range (0, M): # 
            
            if (lt[i][j] != 0):
                dltc = (i**2)+(j**2)
                if (dltc < dlt):
                    plt = (i,j)
                    dlt = dltc
    
            jr = M - j - 1
            if (rt[i][jr] != 0):
                drtc = (i**2)+(j**2)
                if drtc < drt:
                    prt = (i,jr)
                    drt = drtc
                    
            ib = N - i - 1
            if (rb[ib][jr] != 0):
                drbc = (i**2)+(j**2)
                if drbc < drb:
                    prb = (ib,jr)
                    drb = drbc
            
            if (lb[ib][j] != 0):
                dlbc = (i**2)+(j**2)
                if dlbc < dlb:
                    plb = (ib,j)
                    dlb = dlbc
    
    plt = (top - 100 + plt[0], plt[1])
    prt = (top - 100 + prt[0], w-200+prt[1])
    prb = (bot - 100 + prb[0], w-200+prb[1])
    plb = (bot - 100 + plb[0], plb[1])
    
    #print(plt, prt, prb, plb)

    
    dn = 1500
    dm = 3200

    ##  Corrigir a pespectiva
    pts1 = np.float32([[plt[1],plt[0]], [prt[1],prt[0]], [plb[1],plb[0]], [prb[1],prb[0]]])
    pts2 = np.float32([[0,0],[dm,0],[0,dn],[dm,dn]])

    matrix = cv.getPerspectiveTransform(pts1, pts2)
    result = cv.warpPerspective(srcRGB, matrix, (dm, dn))
    #resultGray = cv.cvtColor(result,cv.COLOR_BGR2GRAY)

    #return result, resultGray
    return result

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

def getOptimalDCTSize(N): 
    return 2*cv.getOptimalDFTSize((N+1)//2)

#####   BLOCO PARA NORMALIZAÇÂO DE CORES
#def colorN(srcRGB, srcGray):
def colorN(dstRGB, Ddis = 15):
    h, w, c = dstRGB.shape
    #h_ = getOptimalDCTSize(h);
    #w_ = getOptimalDCTSize(w);
    vis0 = np.ones((h, w, c), np.float64)
    vis0[:h, :w, :] += dstRGB[:, :, :]
    #vis0[h:, :, :] = 255
    #vis0[:, w:, :] = 255
    vis0 = np.log10(vis0)
    for color in range(3):
        vis0[:,:,color] = cv.dct(vis0[:,:,color])
        for i in range(Ddis):
            for j in range(Ddis - i):
                vis0[i, j, color] = 0
        vis0[:,:,color] = cv.idct(vis0[:,:,color])
        vis0[:,:,color] = (10.0**vis0[:,:,color]) - 1
        dstRGB[:, :, color] = cv.normalize(vis0[:h,:w,color], None, 0, 255, cv.NORM_MINMAX, dtype=cv.CV_8U)
    return dstRGB

#####   BLOCO ONDE É REALIZADA A CONVERSÃO PARA YIQ, THRESHOLD E BINARIZAÇÃO
def threshold(dstRGB):

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
            (x_0, y_0) = (i, i)
            break

    #   Preenchimento dos pontos (x_0, y_0)
    cv.floodFill(im_floodfill, mask, (x_0, y_0), 255)

    #   Inverte a Imagem do floodfill
    im_floodfill_inv = cv.bitwise_not(im_floodfill)

    #   Combine as duas imagens para obter a areas de interesse
    im_out = thrGrey | im_floodfill_inv

    #   Encontro os contornos
    contours, hierarchy = cv.findContours(im_out, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    h1, w1 = im_out.shape

    w_soldaP = (1.65*w1)/285
    w_soldaG = (3*w1)/285

    h_soldaP = (1.65*h1)/130
    h_soldaG = (3*h1)/130

    soldaG = w_soldaG * h_soldaG
    soldaP = w_soldaP * h_soldaP

    soldaMh = w_soldaG / h_soldaP
    soldaMw = w_soldaP / h_soldaG

    soldas = 0
    sections = []
    for c in contours:
        M = cv.moments(c)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            x, y, w, h = cv.boundingRect(c)
            #if (abs(w - h) < 25) and ((w * h) < 600) and ((w * h) > 200):
            #if (abs(w - h) < 80) and ((w * h) < 2116) and ((w * h) > 200):
            if ((w / h) >= soldaMw) and ((w / h) <= soldaMh) and ((w * h) <= soldaG) and ((w * h) >= soldaP):
                sections.append((cX, cY, x, y, w, h))
                # cv.circle(img, (cX, cY), 2, (255, 255, 255), -1)
                #cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                if (w>=h):
                    r = w//2
                else:
                    r = h//2
                cv.circle(img, (x+w//2, y+h//2), r, (0, 0, 255), 2)
                soldas = soldas + 1
    print("Quantidade de soldas: ", soldas)

    return img, sections


def main(argv):

    ##  Recebimento dos argumentos
    parser = argparse.ArgumentParser(description = 'Detecção de solda')
    parser.add_argument('--arquivo', action = 'store', dest = 'src', default = 'foto', required = False, help = 'Nome do arquivo de imagem ou "foto" para utilizar a camera')
    parser.add_argument('-filtro', type = int, action = 'store', dest = 'filtro', default = 1, required = False, help = 'Tipo se filtro a ser aplicado: 1- Sem Filtro; 2 - Median Blur; 3 - Gaussian Blur ')
    parser.add_argument('-borda', type = int, action = 'store', dest = 'borda', default = 1, required = False, help = 'Tipo de detecção de borda a ser aplicado: 1- Corner Harris; 2 - Hough Lines')
    
    arguments = parser.parse_args()
    print("Arguments: ", arguments)

    ##  Verifica se carrega o arquivo ou tira uma foto
    if (arguments.src == 'foto'):
        #srcGrey, srcRGB = takepic() #   Chama função da camera
        srcRGB = takepic() #   Chama função da camera
        outFile = "seg_saida.png"
    else:
        #srcGrey, srcRGB = loadImage(arguments.src) # Carrega Imagem
        srcRGB = loadImage(arguments.src) # Carrega Imagem
        # outFile = "seg_" + arguments.src
        outFile = "seg_test.png"
    

    
    ## Aplica o filtro na imagem, caso tenha sido escohido
    #if (arguments.filtro == 2) or (arguments.filtro == 3):
    #    srcGray = filter(srcGrey, arguments.filtro)

    start = time.time()

    ##  Decção de bordas
    if (arguments.borda == 1):
        srcRGB = CornerPespec(srcRGB)
    else:
        edges = edgesDetection(srcGrey)

        #   Detecta a maior borda
        border = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)
        x1, y1, x2, y2 = borderPCB(edges)
        cv.line(border, (x1, y1), (x2, y2), (0, 0, 255), 1, cv.LINE_AA) #   Desenha linha na bordas

        #   Alinhamento
        aliGrey = alignment(srcGrey, x1, y1, x2, y2)
        aliRGB = alignment(srcRGB, x1, y1, x2, y2)

        #   Corta região da placa
        cutGrey = aliGrey[y1:, x1:] 
        cutRGB = aliRGB[y1:, x1:]
        cutGrey = srcGrey
        cutRGB = srcRGB
        
    end = time.time()
    print("Corner")
    print(end - start)
    
    #   Normalização de cor
    #normRGB = colorN(srcRGB, srcGray)
    print(srcRGB.shape)
    normRGB = colorN(srcRGB)

    print("Normal")
    end = time.time()
    print(end - start)

    # Thresholding
    thrGray = threshold(normRGB)

    print("Thresold")
    end = time.time()
    print(end - start)

    img, segList = segment_01(thrGray, normRGB)
    
    end = time.time()
    print(end - start)
    
    cv.imwrite(outFile, img)

    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
