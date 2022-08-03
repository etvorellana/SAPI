import cv2
import numpy as np
from skimage.filters import gabor_kernel

class LogGaborService():
    def __init__(self):
        pass

    def gaborKernel(self, sigmax_init = 3, sigmay_init = 3):
        # theta_init = 0
        # freq_init = 0.1
        kernel_list = []
        kernel_list.append(np.real(gabor_kernel(0.1, 0,sigma_x=sigmax_init, sigma_y=sigmay_init)))
        kernel_list.append(np.real(gabor_kernel(0.3, 0,sigma_x=sigmax_init, sigma_y=sigmay_init)))
        kernel_list.append(np.real(gabor_kernel(0.1, np.pi/4,sigma_x=sigmax_init, sigma_y=sigmay_init)))
        kernel_list.append(np.real(gabor_kernel(0.3, np.pi/4,sigma_x=sigmax_init, sigma_y=sigmay_init)))

        return kernel_list

    def gaborSum(self, img):
        lista_valores = []
        for kernel in self.gaborKernel():
            soma, desvio = self.operacao_gabor(img, kernel)
            lista_valores.append(soma)
            lista_valores.append(desvio)

        return lista_valores

    def operacao_gabor(self, img_solda, kernel):
        img_solda = cv2.cvtColor(img_solda, cv2.COLOR_BGR2GRAY)
        soma = np.sum(cv2.filter2D(img_solda, cv2.CV_8UC3, kernel))
        desvio = np.std(cv2.filter2D(img_solda, cv2.CV_8UC3, kernel))
        return soma, desvio