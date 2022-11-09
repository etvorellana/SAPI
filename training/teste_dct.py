import numpy as np
from csv import reader
import imageio
import sys

sys.path.append('../')
from backend.classification.service.filtros.dct_service import DctService

CLASSIFICACAO_SOLDA_BOA = 0
CLASSIFICACAO_SOLDA_PONTE = 1
CLASSIFICACAO_SOLDA_AUSENTE = 2
CLASSIFICACAO_SOLDA_EXCESSO = 3
CLASSIFICACAO_SOLDA_POUCA = 4

def carrega_img(pasta, lista, x): #Pasta de origem das imagens, lista que as imagens pertecem, numero de imagens
	for i in range(x):
		filename = (pasta + "/Solda_{}.png".format(i+1))
		lista.append(imageio.imread(filename))
	return lista

lista_soldas = []

with open('Dct.csv', 'r') as csv_file:
    csv_reader = reader(csv_file)
    lista_soldas = list(csv_reader)
    #print(lista_soldas)

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

def calculo(l_teste, l_treinamento_boa, l_treinamento_ponte, l_treinamento_ausente, l_treinamento_excesso, l_treinamento_pouca):
    classificacao = []
    classe = [
        CLASSIFICACAO_SOLDA_BOA,
        CLASSIFICACAO_SOLDA_PONTE,
        CLASSIFICACAO_SOLDA_AUSENTE,
        CLASSIFICACAO_SOLDA_EXCESSO,
        CLASSIFICACAO_SOLDA_POUCA
    ]

    mahalanobisResultSoldaBoa = mahalanobis(l_treinamento_boa, l_teste)
    classificacao.append(mahalanobisResultSoldaBoa)

    mahalanobisResultSoldaPonte = mahalanobis(l_treinamento_ponte, l_teste)
    classificacao.append(mahalanobisResultSoldaPonte)

    mahalanobisResultSoldaAusente = mahalanobis(l_treinamento_ausente, l_teste)
    classificacao.append(mahalanobisResultSoldaAusente)

    mahalanobisResultSoldaExcesso = mahalanobis(l_treinamento_excesso, l_teste)
    classificacao.append(mahalanobisResultSoldaExcesso)

    mahalanobisResultSoldaPouca = mahalanobis(l_treinamento_pouca, l_teste)
    classificacao.append(mahalanobisResultSoldaPouca)

    classificacaoIndex = classificacao.index(min(classificacao))

    return classe[classificacaoIndex]

#print("Original: ", lista_soldas[0])
del lista_soldas[0]
#print(lista_soldas[0])

print("Tamanho do conjunto inteiro: ", len(lista_soldas))
#print(lista_soldas)
#print("-------------")

##CONVERTENDO A LISTA DE STRING PARA FLOAT
tam = len(lista_soldas)
for x in range(tam):
    lista_soldas[x] = list(map(float, lista_soldas[x]))

O_soldas_boas = []
O_soldas_excesso = []
O_soldas_ponte = []
O_soldas_pouca = []
O_soldas_ausente = []

carrega_img('Soldas_boas', O_soldas_boas, 200)
carrega_img('Soldas_ponte', O_soldas_ponte, 200)
carrega_img('Soldas_ausente', O_soldas_ausente, 200)
carrega_img('Soldas_excesso', O_soldas_excesso, 200)
carrega_img('Soldas_pouca', O_soldas_pouca, 200)

MRF = np.zeros((5, 5), dtype=float)
TabelaBonita = [["" for x in range(6)]for x in range(6)]
TabelaBonita[0][0] = '       '
TabelaBonita[1][0] = 'Boa    '
TabelaBonita[2][0] = 'Ponte  '
TabelaBonita[3][0] = 'Ausente'
TabelaBonita[4][0] = 'Excesso'
TabelaBonita[5][0] = 'Pouca  '
TabelaBonita[0][1] = 'Boa'
TabelaBonita[0][2] = 'Ponte'
TabelaBonita[0][3] = 'Ausente'
TabelaBonita[0][4] = 'Excesso'
TabelaBonita[0][5] = 'Pouca'
dctService = DctService()
for i in range(200):
    dct_filtered_img = dctService.dct_filter(O_soldas_boas[i])
    lista_valores = dctService.dctSum(dct_filtered_img)
    size = len(lista_soldas)
    classificacao = calculo(lista_valores, lista_soldas[0:int(1/5 * size)], lista_soldas[int(1/5 * size):int(2/5 * size)], lista_soldas[int(2/5 * size):int(3/5 * size)], lista_soldas[int(3/5 * size):int(4/5 * size)], lista_soldas[int(4/5 * size):int(size)])
    MRF[0][classificacao] += 1

for i in range(200):
    dct_filtered_img = dctService.dct_filter(O_soldas_ponte[i])
    lista_valores = dctService.dctSum(dct_filtered_img)
    size = len(lista_soldas)
    classificacao = calculo(lista_valores, lista_soldas[0:int(1/5 * size)], lista_soldas[int(1/5 * size):int(2/5 * size)], lista_soldas[int(2/5 * size):int(3/5 * size)], lista_soldas[int(3/5 * size):int(4/5 * size)], lista_soldas[int(4/5 * size):int(size)])
    MRF[1][classificacao] += 1

for i in range(200):
    dct_filtered_img = dctService.dct_filter(O_soldas_ausente[i])
    lista_valores = dctService.dctSum(dct_filtered_img)
    size = len(lista_soldas)
    classificacao = calculo(lista_valores, lista_soldas[0:int(1/5 * size)], lista_soldas[int(1/5 * size):int(2/5 * size)], lista_soldas[int(2/5 * size):int(3/5 * size)], lista_soldas[int(3/5 * size):int(4/5 * size)], lista_soldas[int(4/5 * size):int(size)])
    MRF[2][classificacao] += 1

for i in range(200):
    dct_filtered_img = dctService.dct_filter(O_soldas_excesso[i])
    lista_valores = dctService.dctSum(dct_filtered_img)
    size = len(lista_soldas)
    classificacao = calculo(lista_valores, lista_soldas[0:int(1/5 * size)], lista_soldas[int(1/5 * size):int(2/5 * size)], lista_soldas[int(2/5 * size):int(3/5 * size)], lista_soldas[int(3/5 * size):int(4/5 * size)], lista_soldas[int(4/5 * size):int(size)])
    MRF[3][classificacao] += 1

for i in range(200):
    dct_filtered_img = dctService.dct_filter(O_soldas_pouca[i])
    lista_valores = dctService.dctSum(dct_filtered_img)
    size = len(lista_soldas)
    classificacao = calculo(lista_valores, lista_soldas[0:int(1/5 * size)], lista_soldas[int(1/5 * size):int(2/5 * size)], lista_soldas[int(2/5 * size):int(3/5 * size)], lista_soldas[int(3/5 * size):int(4/5 * size)], lista_soldas[int(4/5 * size):size])
    MRF[4][classificacao] += 1

for x in range(5):
    for y in range(5):
        MRF[x][y] = (MRF[x][y] * 100) / 200
        TabelaBonita[x+1][y+1] = f'{MRF[x][y]}%'

print("Resutaldo Final: ")
# print(MRF)
for x in range(6):
    linha = ""
    for y in range(6):
        linha += f'{TabelaBonita[x][y]}\t'
    print(linha)