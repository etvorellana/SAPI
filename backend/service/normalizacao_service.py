from model.pcb_flow import PCBFlow
import numpy as np
import cv2 as cv

class NormalizacaoService():
    def tratar(self, pcb_flow : PCBFlow):
        return self.colorN(pcb_flow.img_bordas)

    def colorN(self, dstRGB, Ddis = 15):
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