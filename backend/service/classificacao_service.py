import numpy as np
import cv2
from csv import reader
from skimage.filters import gabor_kernel
from model.pcb_flow import PCBFlow

CLASSIFICACAO_SOLDA_BOA = "Boa"
CLASSIFICACAO_SOLDA_PONTE = "Ponte"
CLASSIFICACAO_SOLDA_AUSENTE = "Ausente"
CLASSIFICACAO_SOLDA_EXCESSO = "Excesso"
CLASSIFICACAO_SOLDA_POUCA = "Pouca"

class ClassificacaoService():
    def __init__(self):
        self.theta_init = 0
        self.freq_init = 0.1
        self.sigmax_init = 3
        self.sigmay_init = 3
        pass

    def classificar(self, pcb_flow : PCBFlow, segList):
        print("Iniciando classificação das soldas...")
        print("Calculando gabor_kernel...")
        kernel_list = []
        kernel_list.append(np.real(gabor_kernel(0.1, 0,sigma_x=self.sigmax_init, sigma_y=self.sigmay_init)))
        kernel_list.append(np.real(gabor_kernel(0.3, 0,sigma_x=self.sigmax_init, sigma_y=self.sigmay_init)))
        kernel_list.append(np.real(gabor_kernel(0.1, np.pi/4,sigma_x=self.sigmax_init, sigma_y=self.sigmay_init)))
        kernel_list.append(np.real(gabor_kernel(0.3, np.pi/4,sigma_x=self.sigmax_init, sigma_y=self.sigmay_init)))

        print("Obtendo base de dados com conjunto de treinamento...")
        lista_base = ClassificacaoService.obter_base_dados()

        print("Classificando cada solda da imagem...")
        soldas = {
            CLASSIFICACAO_SOLDA_BOA: 0,
            CLASSIFICACAO_SOLDA_PONTE: 0,
            CLASSIFICACAO_SOLDA_AUSENTE: 0,
            CLASSIFICACAO_SOLDA_EXCESSO: 0,
            CLASSIFICACAO_SOLDA_POUCA: 0
        }
        for seg in segList:
            cropped_image = pcb_flow.img_norm[seg[3]:seg[3]+seg[5], seg[2]:seg[2]+seg[4]]

            lista_valores = []
            for kernel in kernel_list:
                soma, desvio = ClassificacaoService.operacao_gabor(cropped_image, kernel)
                lista_valores.append(soma)
                lista_valores.append(desvio)

            classificacao = ClassificacaoService.calculo(lista_valores, lista_base[0:200], lista_base[200:400], lista_base[400:600], lista_base[600:800], lista_base[800:1000])

            soldas[classificacao] += 1

        print("Classificação finalizada!")
        return soldas

    def obter_base_dados():
        lista_soldas = []

        with open('media/Gabor_1k.csv', 'r') as csv_file:
            csv_reader = reader(csv_file)
            lista_soldas = list(csv_reader)

        del lista_soldas[0]

        print("Tamanho do conjunto de treinamento: ", len(lista_soldas))

        tam = len(lista_soldas)
        for x in range(tam):
            lista_soldas[x] = list(map(float, lista_soldas[x]))

        return lista_soldas

    def operacao_gabor(img_solda, kernel):
        img_solda = cv2.cvtColor(img_solda, cv2.COLOR_BGR2GRAY)
        soma = np.sum(cv2.filter2D(img_solda, cv2.CV_8UC3, kernel))
        desvio = np.std(cv2.filter2D(img_solda, cv2.CV_8UC3, kernel))
        return soma, desvio

    def calculo(l_teste, l_treinamento_boa, l_treinamento_pouca, l_treinamento_ponte, l_treinamento_excesso, l_treinamento_ausente):
        classificacao = []
        classe = [CLASSIFICACAO_SOLDA_BOA, CLASSIFICACAO_SOLDA_PONTE, CLASSIFICACAO_SOLDA_AUSENTE, CLASSIFICACAO_SOLDA_EXCESSO, CLASSIFICACAO_SOLDA_POUCA]

        mahalanobisResultSoldaBoa = ClassificacaoService.mahalanobis(l_treinamento_boa, l_teste)
        classificacao.append(mahalanobisResultSoldaBoa)

        mahalanobisResultSoldaPonte = ClassificacaoService.mahalanobis(l_treinamento_ponte, l_teste)
        classificacao.append(mahalanobisResultSoldaPonte)

        mahalanobisResultSoldaAusente = ClassificacaoService.mahalanobis(l_treinamento_ausente, l_teste)
        classificacao.append(mahalanobisResultSoldaAusente)

        mahalanobisResultSoldaExcesso = ClassificacaoService.mahalanobis(l_treinamento_excesso, l_teste)
        classificacao.append(mahalanobisResultSoldaExcesso)

        mahalanobisResultSoldaPouca = ClassificacaoService.mahalanobis(l_treinamento_pouca, l_teste)
        classificacao.append(mahalanobisResultSoldaPouca)

        classificacaoIndex = classificacao.index(min(classificacao))

        return classe[classificacaoIndex]

    def mahalanobis(data, x):
        m = np.mean(data, axis = 0)

        xMm = x - m

        data = np.transpose(data)
        covM = np.cov(data, bias = False)
        invCoveM = np.linalg.inv(covM)

        np.set_printoptions(suppress=True)

        tem1 = np.dot(xMm, invCoveM)
        tem2 = np.dot(tem1, np.transpose(xMm))
        MD = np.sqrt(tem2)

        result = np.reshape(MD, -1)
        return result