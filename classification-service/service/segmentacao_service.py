from model.pcb_flow import PCBFlow
import numpy as np
import cv2 as cv
import json

from service.classificacao_service import ClassificacaoService
from service.threshold_service import ThresholdService
import model.constantes as constantes

classificacao_service = ClassificacaoService()

class SegmentacaoService():

    def segment_area(self, thrGrey):
        newsections = []

        #   Encontro os contornos
        contours, hierarchy = cv.findContours(thrGrey, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        for c in contours:
            M = cv.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                x, y, w, h = cv.boundingRect(c)
                newsections.append((cX, cY, x, y, w, h))

        return newsections

    def tratar(self, pcb_flow : PCBFlow):
        
        soldas = {
            constantes.CLASSIFICACAO_SOLDA_BOA[0]: 0,
            constantes.CLASSIFICACAO_SOLDA_PONTE[0]: 0,
            constantes.CLASSIFICACAO_SOLDA_AUSENTE[0]: 0,
            constantes.CLASSIFICACAO_SOLDA_EXCESSO[0]: 0,
            constantes.CLASSIFICACAO_SOLDA_POUCA[0]: 0
        }

        thrGrey, scrRGB = pcb_flow.thrGray, pcb_flow.img_bordas
        #   Copia a imagem com o limiar
        im_floodfill = thrGrey.copy()
        img = scrRGB.copy()
        
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)


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

        w_soldaP = (0.95*w1)/285
        w_soldaG = (3.04*w1)/285

        h_soldaP = (0.95*h1)/130
        h_soldaG = (3.04*h1)/130

        soldaG = w_soldaG * h_soldaG
        soldaP = w_soldaP * h_soldaP

        soldaMh = w_soldaG / h_soldaP
        soldaMw = w_soldaP / h_soldaG

        #   Dimensões das possiveis areas com soldas
        w_areaP = (2*w1)/285
        w_areaG = (8*w1)/285

        h_areaP = (2*h1)/130
        h_areaG = (8*h1)/130

        areaG = w_areaG * h_areaG
        areaP = w_areaP * h_areaP

        areaMh = w_areaG / h_areaP
        areaMw = w_areaP / h_areaG

        qtd_soldas = 0

        thresholdService : ThresholdService = ThresholdService()

        for c in contours:
            M = cv.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                x, y, w, h = cv.boundingRect(c)
                if ((w / h) >= soldaMw) and ((w / h) <= soldaMh) and ((w * h) <= soldaG) and ((w * h) >= soldaP):
                    section_info = (cX, cY, x, y, w, h)
                    if (w>=h):
                        r = w//2
                    else:
                        r = h//2

                    classificacao = classificacao_service.classificar(pcb_flow, section_info)
                    
                    soldas[classificacao[0]] += 1
                    qtd_soldas += 1
                    
                    cv.circle(img, (x+w//2, y+h//2), r, classificacao[1], 2)
                elif ((w / h) >= areaMw) and ((w / h) <= areaMh) and ((w * h) <= areaG) and ((w * h) >= areaP):
                    section_info = (cX, cY, x, y, w, h)
                    if (w>=h):
                        r = w//2
                    else:
                        r = h//2
                    area = pcb_flow.img_norm[section_info[3]:section_info[3]+section_info[5], section_info[2]:section_info[2]+section_info[4]]
                    area_thr = thresholdService.threshold(area)
                    aux = self.segment_area(area_thr)
                    if len(aux) != 0:
                        tam = len(aux)
                        for x in range (tam):
                            cX_N = section_info[0] + aux[x][0]
                            cY_N = section_info[1] + aux[x][1]
                            x_N = section_info[2] + aux[x][2]
                            y_N = section_info[3] + aux[x][3]
                            w_N = aux[x][4]
                            h_N = aux[x][5]

                            section_info = (cX_N, cY_N, x_N, y_N, w_N, h_N)

                            classificacao = classificacao_service.classificar(pcb_flow, section_info)

                            soldas[classificacao[0]] += 1
                            qtd_soldas += 1
                            cv.circle(img, (x_N+w_N//2, y_N+h_N//2), r, classificacao[1], 2)

        print("Quantidade de soldas: ", qtd_soldas)
        
        print(json.dumps(soldas))

        return img, soldas, qtd_soldas