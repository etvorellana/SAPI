import numpy as np
import cv2
from csv import reader
from service.filtros.dct_service import DctService
from service.filtros.log_gabor_service import LogGaborService
from model.pcb_flow import PCBFlow
import model.constantes as constantes

class ClassificacaoService():
    def __init__(self):
        self.lista_base = ClassificacaoService.obter_base_dados()

    def classificar(self, pcb_flow : PCBFlow, segment, filter = 2):
        cropped_image = pcb_flow.img_bordas[segment[3]:segment[3]+segment[5], segment[2]:segment[2]+segment[4]]
        lista_valores = []

        print("Aplicando filtro...")
        if filter == 1:
            gaborService = LogGaborService()
            lista_valores = gaborService.gaborSum(cropped_image)
        elif filter == 2:
            dctService = DctService()
            lista_valores = dctService.dctSum(cropped_image)
        else:
            print("Filtro não informado!")
            return

        print("Classificando...")

        classificacao = ClassificacaoService.calculo(lista_valores, self.lista_base[0:200], self.lista_base[200:400], self.lista_base[400:600], self.lista_base[600:800], self.lista_base[800:1000])

        return classificacao

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

    def calculo(l_teste, l_treinamento_boa, l_treinamento_pouca, l_treinamento_ponte, l_treinamento_excesso, l_treinamento_ausente):
        classificacao = []
        classe = [
            constantes.CLASSIFICACAO_SOLDA_BOA,
            constantes.CLASSIFICACAO_SOLDA_PONTE,
            constantes.CLASSIFICACAO_SOLDA_AUSENTE,
            constantes.CLASSIFICACAO_SOLDA_EXCESSO,
            constantes.CLASSIFICACAO_SOLDA_POUCA
        ]

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