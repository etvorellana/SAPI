from model.pcb_flow import PCBFlow
import numpy as np
import cv2 as cv

class SegmentacaoService():
    def tratar(self, pcb_flow : PCBFlow):
        return self.segment_01(pcb_flow.thrGray, pcb_flow.img_norm)

    def segment_01(self, thrGrey, normRGB):
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
                    cv.circle(img, (x+w//2, y+h//2), r, (255, 0, 0), 2)
                    soldas = soldas + 1
        print("Quantidade de soldas: ", soldas)

        return img, sections