from model.pcb_flow import PCBFlow
from .alinhamento_service import AlinhamentoService
import numpy as np
import cv2 as cv

alinhamentoService : AlinhamentoService = AlinhamentoService()

class DeteccaoBordasService:
    def tratar(self, pcb_flow : PCBFlow):
        ##  Decção de bordas
        if (pcb_flow.borda == 1):
            srcRGB = self.CornerPespec(pcb_flow.img_src)
            return srcRGB
        else:
            edges = self.edgesDetection(srcGrey)

            #   Detecta a maior borda
            border = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)
            x1, y1, x2, y2 = self.borderPCB(edges)
            cv.line(border, (x1, y1), (x2, y2), (0, 0, 255), 1, cv.LINE_AA) #   Desenha linha na bordas

            #   Alinhamento
            aliGrey = alinhamentoService.alignment(srcGrey, x1, y1, x2, y2)
            aliRGB = alinhamentoService.alignment(srcRGB, x1, y1, x2, y2)

            #   Corta região da placa
            cutGrey = aliGrey[y1:, x1:] 
            cutRGB = aliRGB[y1:, x1:]
            cutGrey = srcGrey
            cutRGB = srcRGB

            # return srcRGB

    ## Detecção de cantos e correção de pespectiva com corner Harris
    def CornerPespec(self, srcRGB):
        
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