from random import shuffle
import numpy as np
import cv2
from csv import reader
import imageio

from dct import dct_filter, dctSum

CLASSIFICACAO_SOLDA_BOA = "Boa"
CLASSIFICACAO_SOLDA_PONTE = "Ponte"
CLASSIFICACAO_SOLDA_AUSENTE = "Ausente"
CLASSIFICACAO_SOLDA_EXCESSO = "Excesso"
CLASSIFICACAO_SOLDA_POUCA = "Pouca"

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

# colocando em escala de cinza
for i in range(200):
	O_soldas_boas[i] = cv2.cvtColor(O_soldas_boas[i], cv2.COLOR_BGR2GRAY)

for i in range(200):
	# O_soldas_boas[i] = cv2.cvtColor(O_soldas_boas[i], cv2.COLOR_BGR2GRAY)
	O_soldas_ponte[i] = cv2.cvtColor(O_soldas_ponte[i], cv2.COLOR_BGR2GRAY)
	O_soldas_ausente[i] = cv2.cvtColor(O_soldas_ausente[i], cv2.COLOR_BGR2GRAY)
	O_soldas_excesso[i] = cv2.cvtColor(O_soldas_excesso[i], cv2.COLOR_BGR2GRAY)
	O_soldas_pouca[i] = cv2.cvtColor(O_soldas_pouca[i], cv2.COLOR_BGR2GRAY)

corretas_boas = 0
deu_ruim_boas = 0
corretas_ponte = 0
deu_ruim_ponte = 0
corretas_ausente = 0
deu_ruim_ausente = 0
corretas_excesso = 0
deu_ruim_excesso = 0
corretas_pouca = 0
deu_ruim_pouca = 0
for i in range(200):
    dct_filtered_img = dct_filter(O_soldas_boas[i])
    lista_valores = dctSum(dct_filtered_img)
    size = len(lista_soldas)
    classificacao = calculo(lista_valores, lista_soldas[0:int(1/5 * size)], lista_soldas[int(1/5 * size):int(2/5 * size)], lista_soldas[int(2/5 * size):int(3/5 * size)], lista_soldas[int(3/5 * size):int(4/5 * size)], lista_soldas[int(4/5 * size):int(size)])
    if classificacao == CLASSIFICACAO_SOLDA_BOA:
        corretas_boas += 1
    else:
        deu_ruim_boas += 1

for i in range(200):
    dct_filtered_img = dct_filter(O_soldas_ponte[i])
    lista_valores = dctSum(dct_filtered_img)
    size = len(lista_soldas)
    classificacao = calculo(lista_valores, lista_soldas[0:int(1/5 * size)], lista_soldas[int(1/5 * size):int(2/5 * size)], lista_soldas[int(2/5 * size):int(3/5 * size)], lista_soldas[int(3/5 * size):int(4/5 * size)], lista_soldas[int(4/5 * size):int(size)])
    if classificacao == CLASSIFICACAO_SOLDA_PONTE:
        corretas_ponte += 1
    else:
        deu_ruim_ponte += 1

for i in range(200):
    dct_filtered_img = dct_filter(O_soldas_ausente[i])
    lista_valores = dctSum(dct_filtered_img)
    size = len(lista_soldas)
    classificacao = calculo(lista_valores, lista_soldas[0:int(1/5 * size)], lista_soldas[int(1/5 * size):int(2/5 * size)], lista_soldas[int(2/5 * size):int(3/5 * size)], lista_soldas[int(3/5 * size):int(4/5 * size)], lista_soldas[int(4/5 * size):int(size)])
    if classificacao == CLASSIFICACAO_SOLDA_AUSENTE:
        corretas_ausente += 1
    else:
        deu_ruim_ausente += 1

for i in range(200):
    dct_filtered_img = dct_filter(O_soldas_excesso[i])
    lista_valores = dctSum(dct_filtered_img)
    size = len(lista_soldas)
    classificacao = calculo(lista_valores, lista_soldas[0:int(1/5 * size)], lista_soldas[int(1/5 * size):int(2/5 * size)], lista_soldas[int(2/5 * size):int(3/5 * size)], lista_soldas[int(3/5 * size):int(4/5 * size)], lista_soldas[int(4/5 * size):int(size)])
    if classificacao == CLASSIFICACAO_SOLDA_EXCESSO:
        corretas_excesso += 1
    else:
        deu_ruim_excesso += 1

for i in range(200):
    dct_filtered_img = dct_filter(O_soldas_pouca[i])
    lista_valores = dctSum(dct_filtered_img)
    size = len(lista_soldas)
    classificacao = calculo(lista_valores, lista_soldas[0:int(1/5 * size)], lista_soldas[int(1/5 * size):int(2/5 * size)], lista_soldas[int(2/5 * size):int(3/5 * size)], lista_soldas[int(3/5 * size):int(4/5 * size)], lista_soldas[int(4/5 * size):size])
    if classificacao == CLASSIFICACAO_SOLDA_POUCA:
        corretas_pouca += 1
    else:
        deu_ruim_pouca += 1

print("Resutaldo Final: ")
print(f"Corretas boas: {corretas_boas}")
print(f"Deu ruim boas: {deu_ruim_boas}")
print(f"Corretas ponte: {corretas_ponte}")
print(f"Deu ruim ponte: {deu_ruim_ponte}")
print(f"Corretas ausente: {corretas_ausente}")
print(f"Deu ruim ausente: {deu_ruim_ausente}")
print(f"Corretas excesso: {corretas_excesso}")
print(f"Deu ruim excesso: {deu_ruim_excesso}")
print(f"Corretas pouca: {corretas_pouca}")
print(f"Deu ruim pouca: {deu_ruim_pouca}")
print(f"Corretas total: {corretas_boas + corretas_ponte + corretas_ausente + corretas_excesso + corretas_pouca}")
print(f"Deu ruim total: {deu_ruim_boas + deu_ruim_ponte + deu_ruim_ausente + deu_ruim_excesso + deu_ruim_pouca}")