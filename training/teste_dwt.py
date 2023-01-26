import numpy as np
# from csv import reader
import pandas as pd
import imageio
import sys

sys.path.append('../')
from backend.classification.service.filtros.dwt_service import DwtService

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
lista_teste = []

print("========================")
with open('DwtKF1.csv', 'r') as csv_file:
    #csv_reader = reader(csv_file)
    csv_reader = pd.read_csv(csv_file)
    lista_soldas = csv_reader.iloc[:,1:].values
    #lista_soldas = list(csv_reader)
    print(lista_soldas.shape)
    print(type(lista_soldas))  
print("========================")
with open('DwtKF1t.csv', 'r') as csv_file:
    #csv_reader = reader(csv_file)
    csv_reader = pd.read_csv(csv_file)
    lista_teste = csv_reader.iloc[:,1:].values
    #lista_teste = list(csv_reader)
    print(lista_teste.shape)
    print(type(lista_teste))  
print("========================")

def mahalanobisPar(data):
    m = np.mean(data, axis = 0)

    dataT = np.transpose(data)
    covM = np.cov(dataT, bias = False)
    invCoveM = np.linalg.inv(covM)
    return m, invCoveM

def mahalanobis(m, invCoveM, x):
    #m = np.mean(data, axis = 0)

    xMm = x - m

    #data = np.transpose(data)
    #covM = np.cov(data, bias = False)
    #invCoveM = np.linalg.inv(covM)

    np.set_printoptions(suppress=True)

    tem1 = np.dot(xMm, invCoveM)
    tem2 = np.dot(tem1, np.transpose(xMm))
    MD = np.sqrt(tem2)

    result = np.reshape(MD, -1)
    return result

def calculo(l_teste, mBoa, invCoveMBoa, mPonte, invCoveMPonte, 
            mAusente, invCoveMAusente, mExcesso, invCoveMExcesso, 
            mPouca, invCoveMPouca):
    classificacao = []
    classe = [
        CLASSIFICACAO_SOLDA_BOA,
        CLASSIFICACAO_SOLDA_PONTE,
        CLASSIFICACAO_SOLDA_AUSENTE,
        CLASSIFICACAO_SOLDA_EXCESSO,
        CLASSIFICACAO_SOLDA_POUCA
    ]
    #mBoa, invCoveMBoa = mahalanobisPar(l_treinamento_boa)
    mahalanobisResultSoldaBoa = mahalanobis(mBoa, invCoveMBoa, l_teste)
    classificacao.append(mahalanobisResultSoldaBoa)

    #mPonte, invCoveMPonte = mahalanobisPar(l_treinamento_ponte)
    mahalanobisResultSoldaPonte = mahalanobis(mPonte, invCoveMPonte, l_teste)
    classificacao.append(mahalanobisResultSoldaPonte)

    #mAusente, invCoveMAusente = mahalanobisPar(l_treinamento_ausente)
    mahalanobisResultSoldaAusente = mahalanobis(mAusente, invCoveMAusente, l_teste)
    classificacao.append(mahalanobisResultSoldaAusente)

    #mExcesso, invCoveMExcesso = mahalanobisPar(l_treinamento_excesso)
    mahalanobisResultSoldaExcesso = mahalanobis(mExcesso, invCoveMExcesso, l_teste)
    classificacao.append(mahalanobisResultSoldaExcesso)

    #mPouca, invCoveMPouca = mahalanobisPar(l_treinamento_pouca)
    mahalanobisResultSoldaPouca = mahalanobis(mPouca, invCoveMPouca, l_teste)
    classificacao.append(mahalanobisResultSoldaPouca)

    classificacaoIndex = classificacao.index(min(classificacao))

    return classe[classificacaoIndex]

#print("Original: ", lista_soldas[0])
# del lista_soldas[0]
#print(lista_soldas[0])

# print("Tamanho do conjunto inteiro: ", len(lista_soldas))
#print(lista_soldas)
#print("-------------")

##CONVERTENDO A LISTA DE STRING PARA FLOAT
# tam = len(lista_soldas)
# for x in range(tam):
#     lista_soldas[x] = list(map(float, lista_soldas[x]))

# O_soldas_boas = []
# O_soldas_excesso = []
# O_soldas_ponte = []
# O_soldas_pouca = []
# O_soldas_ausente = []

# carrega_img('Soldas_boas', O_soldas_boas, 200)
# carrega_img('Soldas_ponte', O_soldas_ponte, 200)
# carrega_img('Soldas_ausente', O_soldas_ausente, 200)
# carrega_img('Soldas_excesso', O_soldas_excesso, 200)
# carrega_img('Soldas_pouca', O_soldas_pouca, 200)

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
dwtService = DwtService()

classSize, nClasses = lista_soldas.shape
classSize = int (classSize/5)
print("classSize = " + str(classSize))
mBoa, invCoveMBoa = mahalanobisPar(lista_soldas[:classSize])
print(lista_soldas[:classSize].shape)
mPonte, invCoveMPonte = mahalanobisPar(lista_soldas[classSize:2*classSize])
print(lista_soldas[classSize:2*classSize].shape)
mAusente, invCoveMAusente = mahalanobisPar(lista_soldas[2*classSize:3*classSize])
print(lista_soldas[2*classSize:3*classSize].shape)
mExcesso, invCoveMExcesso = mahalanobisPar(lista_soldas[3*classSize:4*classSize])
print(lista_soldas[3*classSize:4*classSize].shape)
mPouca, invCoveMPouca = mahalanobisPar(lista_soldas[4*classSize:])
print(lista_soldas[4*classSize:].shape)
print("Boa: " + str(mBoa))
print("Ponte: " + str(mPonte))
print("Ausente:  " + str(mAusente))
print("Excesso: " + str(mExcesso))
print("Pouca: " +  str(mPouca))

testeSize, nClasses = lista_teste.shape
testeSize = int (testeSize/5)
print("testeSize = " + str(testeSize))
for i in range(testeSize):
    # dwt_filtered_img = dwtService.dwt_filter(O_soldas_boas[i])
    # lista_valores = dwtService.dwtSum(dwt_filtered_img)
    # size = len(lista_soldas)
    # classificacao = calculo(lista_valores, lista_soldas[0:int(1/5 * size)], lista_soldas[int(1/5 * size):int(2/5 * size)], lista_soldas[int(2/5 * size):int(3/5 * size)], lista_soldas[int(3/5 * size):int(4/5 * size)], lista_soldas[int(4/5 * size):int(size)])
    lista_valores = lista_teste[i]
    classificacao = calculo(lista_valores,  mBoa, invCoveMBoa, 
                                            mPonte, invCoveMPonte, 
                                            mAusente, invCoveMAusente, 
                                            mExcesso, invCoveMExcesso, 
                                            mPouca, invCoveMPouca)
    MRF[0][classificacao] += 1

for i in range(testeSize):
    # dwt_filtered_img = dwtService.dwt_filter(O_soldas_ponte[i])
    # lista_valores = dwtService.dwtSum(dwt_filtered_img)
    # size = len(lista_soldas)
    # classificacao = calculo(lista_valores, lista_soldas[0:int(1/5 * size)], lista_soldas[int(1/5 * size):int(2/5 * size)], lista_soldas[int(2/5 * size):int(3/5 * size)], lista_soldas[int(3/5 * size):int(4/5 * size)], lista_soldas[int(4/5 * size):int(size)])
    lista_valores = lista_teste[testeSize+i]
    classificacao = calculo(lista_valores,  mBoa, invCoveMBoa, 
                                            mPonte, invCoveMPonte, 
                                            mAusente, invCoveMAusente, 
                                            mExcesso, invCoveMExcesso, 
                                            mPouca, invCoveMPouca)
    MRF[1][classificacao] += 1

for i in range(testeSize):
    # dwt_filtered_img = dwtService.dwt_filter(O_soldas_ausente[i])
    # lista_valores = dwtService.dwtSum(dwt_filtered_img)
    # size = len(lista_soldas)
    # classificacao = calculo(lista_valores, lista_soldas[0:int(1/5 * size)], lista_soldas[int(1/5 * size):int(2/5 * size)], lista_soldas[int(2/5 * size):int(3/5 * size)], lista_soldas[int(3/5 * size):int(4/5 * size)], lista_soldas[int(4/5 * size):int(size)])
    lista_valores = lista_teste[2*testeSize+i]
    classificacao = calculo(lista_valores,  mBoa, invCoveMBoa, 
                                            mPonte, invCoveMPonte, 
                                            mAusente, invCoveMAusente, 
                                            mExcesso, invCoveMExcesso, 
                                            mPouca, invCoveMPouca)
    MRF[2][classificacao] += 1

for i in range(testeSize):
    # dwt_filtered_img = dwtService.dwt_filter(O_soldas_excesso[i])
    # lista_valores = dwtService.dwtSum(dwt_filtered_img)
    # size = len(lista_soldas)
    # classificacao = calculo(lista_valores, lista_soldas[0:int(1/5 * size)], lista_soldas[int(1/5 * size):int(2/5 * size)], lista_soldas[int(2/5 * size):int(3/5 * size)], lista_soldas[int(3/5 * size):int(4/5 * size)], lista_soldas[int(4/5 * size):int(size)])
    lista_valores = lista_teste[3*testeSize+i]
    classificacao = calculo(lista_valores,  mBoa, invCoveMBoa, 
                                            mPonte, invCoveMPonte, 
                                            mAusente, invCoveMAusente, 
                                            mExcesso, invCoveMExcesso, 
                                            mPouca, invCoveMPouca)
    MRF[3][classificacao] += 1

for i in range(testeSize):
    # dwt_filtered_img = dwtService.dwt_filter(O_soldas_pouca[i])
    # lista_valores = dwtService.dwtSum(dwt_filtered_img)
    # size = len(lista_soldas)
    # classificacao = calculo(lista_valores, lista_soldas[0:int(1/5 * size)], lista_soldas[int(1/5 * size):int(2/5 * size)], lista_soldas[int(2/5 * size):int(3/5 * size)], lista_soldas[int(3/5 * size):int(4/5 * size)], lista_soldas[int(4/5 * size):size])
    lista_valores = lista_teste[4*testeSize+i] 
    classificacao = calculo(lista_valores,  mBoa, invCoveMBoa, 
                                            mPonte, invCoveMPonte, 
                                            mAusente, invCoveMAusente, 
                                            mExcesso, invCoveMExcesso, 
                                            mPouca, invCoveMPouca)
    MRF[4][classificacao] += 1

for x in range(5):
    for y in range(5):
        MRF[x][y] = (MRF[x][y] * 100) / testeSize
        TabelaBonita[x+1][y+1] = f'{MRF[x][y]}%'

print("Resutaldo Final: ")
# print(MRF)
for x in range(6):
    linha = ""
    for y in range(6):
        linha += f'{TabelaBonita[x][y]}\t'
    print(linha)