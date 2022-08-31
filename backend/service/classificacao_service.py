import numpy as np
from csv import reader
from service.filtros.dct_service import DctService
from service.filtros.log_gabor_service import LogGaborService
from model.pcb_flow import PCBFlow
import model.constantes as constantes

class ClassificacaoService():
    def __init__(self):
        self.lista_base_gabor, self.lista_base_dct = ClassificacaoService.obter_base_dados()

    def classificar(self, pcb_flow : PCBFlow, segment):
        lista_valores = []

        if pcb_flow.filtro == 1:
            cropped_image = pcb_flow.img_bordas[segment[3]:segment[3]+segment[5], segment[2]:segment[2]+segment[4]]
            gaborService = LogGaborService()
            lista_valores = gaborService.gaborSum(cropped_image)
            classificacao = ClassificacaoService.calculo(lista_valores, self.lista_base_gabor[0:200], self.lista_base_gabor[200:400], self.lista_base_gabor[400:600], self.lista_base_gabor[600:800], self.lista_base_gabor[800:1000])
        elif pcb_flow.filtro == 2:
            dctService = DctService()
            dct_filtered_img = dctService.dct_filter(pcb_flow.img_bordas)
            cropped_image = dct_filtered_img[segment[3]:segment[3]+segment[5], segment[2]:segment[2]+segment[4]]
            lista_valores = dctService.dctSum(cropped_image)
            classificacao = ClassificacaoService.calculo(lista_valores, self.lista_base_dct[0:200], self.lista_base_dct[200:400], self.lista_base_dct[400:600], self.lista_base_dct[600:800], self.lista_base_dct[800:1000])
        elif pcb_flow.filtro == 3:
            pass
        else:
            print("Filtro inválido!")
            return

        return classificacao

    def obter_base_dados():
        lista_soldas_gabor = []
        lista_soldas_dct = []

        with open('media/Gabor_1k.csv', 'r') as csv_file:
            csv_reader = reader(csv_file)
            lista_soldas_gabor = list(csv_reader)

        with open('media/Dct.csv', 'r') as csv_file:
            csv_reader = reader(csv_file)
            lista_soldas_dct = list(csv_reader)

        del lista_soldas_gabor[0]
        del lista_soldas_dct[0]

        print("Tamanho do conjunto de treinamento gabor: ", len(lista_soldas_gabor))
        print("Tamanho do conjunto de treinamento dct: ", len(lista_soldas_dct))

        tam = len(lista_soldas_gabor)
        for x in range(tam):
            lista_soldas_gabor[x] = list(map(float, lista_soldas_gabor[x]))

        tam = len(lista_soldas_dct)
        for x in range(tam):
            lista_soldas_dct[x] = list(map(float, lista_soldas_dct[x]))

        return lista_soldas_gabor, lista_soldas_dct

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