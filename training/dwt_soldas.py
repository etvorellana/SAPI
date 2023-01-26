import pandas as pd
import numpy as np
import imageio
import sys
import random

sys.path.append('../')
from backend.classification.service.filtros.dwt_service import DwtService

###Carrega as imagens

def carrega_img(pasta, lista, x): #Pasta de origem das imagens, lista que as imagens pertecem, numero de imagens
	for i in range(x):
		filename = (pasta + "/Solda_{}.png".format(i+1))
		lista.append(imageio.imread(filename))
	return lista

### Listas com as imagens
size = 4464*5
size_treinamento = 20000
size_teste = 464*4
kfold_treinamento = 15000
kfold_teste = 5000
size_caracteristicas = 5

images = np.zeros((size, size_caracteristicas))

L_soma = []
L_desvio = []
L_media = []
L_max = []
L_min = []

O_soldas_boas = []
O_soldas_excesso = []
O_soldas_ponte = []
O_soldas_pouca = []
O_soldas_ausente = []

carrega_img('Soldas_boas', O_soldas_boas, 4464)
carrega_img('Soldas_ponte', O_soldas_ponte, 4464)
carrega_img('Soldas_ausente', O_soldas_ausente, 4464)
carrega_img('Soldas_excesso', O_soldas_excesso, 4464)
carrega_img('Soldas_pouca', O_soldas_pouca, 4464)

random.shuffle(O_soldas_boas)
random.shuffle(O_soldas_ponte)
random.shuffle(O_soldas_ausente)
random.shuffle(O_soldas_excesso)
random.shuffle(O_soldas_pouca)

iniBoa = 0
iniPonte = 4464
iniAusente = 4464*2
iniExcesso = 4464*3
iniPouca = 4464*4

dwtService = DwtService()
###########################################
####### Operações com as soldas boas ######
###########################################
for i in range(4464):
	dwt_filtered_img = dwtService.dwt_filter(O_soldas_boas[i])
	lista_valores = dwtService.dwtSum(dwt_filtered_img)
	images[iniBoa + i] = lista_valores

##############################################
####### Operações com as soldas em ponte #####
##############################################
for i in range(4464):
	dwt_filtered_img = dwtService.dwt_filter(O_soldas_ponte[i])
	lista_valores = dwtService.dwtSum(dwt_filtered_img)
	images[iniPonte + i] = lista_valores

#############################################
####### Operações com as soldas ausente #####
#############################################
for i in range(4464):
	dwt_filtered_img = dwtService.dwt_filter(O_soldas_ausente[i])
	lista_valores = dwtService.dwtSum(dwt_filtered_img)
	images[iniAusente + i] = lista_valores

#############################################
####### Operações com as soldas excesso #####
#############################################
for i in range(4464):
	dwt_filtered_img = dwtService.dwt_filter(O_soldas_excesso[i])
	lista_valores = dwtService.dwtSum(dwt_filtered_img)
	images[iniExcesso + i] = lista_valores

##########################################
####### Operações com as soldas pouca ####
##########################################
for i in range(4464):
	dwt_filtered_img = dwtService.dwt_filter(O_soldas_pouca[i])
	lista_valores = dwtService.dwtSum(dwt_filtered_img)
	images[iniPouca + i] = lista_valores

kfold_treino = np.zeros((15000,size_caracteristicas))
kfold_treino[:3000] = images[iniBoa + 1000:iniBoa + 4000]
kfold_treino[3000:6000] = images[iniPonte + 1000:iniPonte + 4000]
kfold_treino[6000:9000] = images[iniAusente + 1000:iniAusente + 4000]
kfold_treino[9000:12000] = images[iniExcesso + 1000:iniExcesso + 4000]
kfold_treino[12000:15000] = images[iniPouca + 1000:iniPouca + 4000]

df = pd.DataFrame(np.column_stack([kfold_treino]), 
					columns=['Soma', 'Media', 'Desvio Padrão', 'Min', 'Max'])
df.to_csv('DwtKF1.csv', encoding='utf-8', index=False)
kfold_teste = np.zeros((5000,size_caracteristicas))
kfold_teste[:1000] = images[iniBoa:iniBoa + 1000] 
kfold_teste[1000:2000] = images[iniPonte:iniPonte + 1000]
kfold_teste[2000:3000] = images[iniAusente:iniAusente + 1000]
kfold_teste[3000:4000] = images[iniExcesso:iniExcesso + 1000]
kfold_teste[4000:5000] = images[iniPouca:iniPouca + 1000]

df = pd.DataFrame(np.column_stack([kfold_teste]), 
					columns=['Soma', 'Media', 'Desvio Padrão', 'Min', 'Max'])
df.to_csv('DwtKF1t.csv', encoding='utf-8', index=False)
kfold_treino[:1000] = images[iniBoa:iniBoa + 1000] 
kfold_treino[1000:3000] = images[iniBoa + 2000:iniBoa + 4000]
kfold_treino[3000:4000] = images[iniPonte:iniPonte + 1000]
kfold_treino[4000:6000] = images[iniPonte + 2000:iniPonte + 4000]
kfold_treino[6000:7000] = images[iniAusente:iniAusente + 1000]
kfold_treino[7000:9000] = images[iniAusente + 2000:iniAusente + 4000]
kfold_treino[9000:10000] = images[iniExcesso:iniExcesso + 1000]
kfold_treino[10000:12000] = images[iniExcesso + 2000:iniExcesso + 4000]
kfold_treino[12000:13000] = images[iniPouca:iniPouca + 1000]
kfold_treino[13000:15000] = images[iniPouca + 2000:iniPouca + 4000]

df = pd.DataFrame(np.column_stack([kfold_treino]), 
					columns=['Soma', 'Media', 'Desvio Padrão', 'Min', 'Max'])
df.to_csv('DwtKF2.csv', encoding='utf-8', index=False)
kfold_teste[:1000] = images[iniBoa + 1000:iniBoa + 2000] 
kfold_teste[1000:2000] = images[iniPonte + 1000:iniPonte + 2000]
kfold_teste[2000:3000] = images[iniAusente + 1000:iniAusente +2000]
kfold_teste[3000:4000] = images[iniExcesso + 1000:iniExcesso + 2000]
kfold_teste[4000:5000] = images[iniPouca + 1000:iniPouca + 2000]

df = pd.DataFrame(np.column_stack([kfold_teste]), 
					columns=['Soma', 'Media', 'Desvio Padrão', 'Min', 'Max'])
df.to_csv('DwtKF2t.csv', encoding='utf-8', index=False)
kfold_treino[:2000] = images[iniBoa:iniBoa + 2000]
kfold_treino[2000:3000] = images[iniBoa + 3000:iniBoa + 4000]
kfold_treino[3000:5000] = images[iniPonte:iniPonte + 2000]
kfold_treino[5000:6000] = images[iniPonte + 3000:iniPonte + 4000]
kfold_treino[6000:8000] = images[iniAusente:iniAusente + 2000]
kfold_treino[8000:9000] = images[iniAusente + 3000:iniAusente + 4000]
kfold_treino[9000:11000] = images[iniExcesso:iniExcesso + 2000]
kfold_treino[11000:12000] = images[iniExcesso + 3000:iniExcesso + 4000]
kfold_treino[12000:14000] = images[iniPouca:iniPouca + 2000]
kfold_treino[14000:15000] = images[iniPouca + 3000:iniPouca + 4000]

df = pd.DataFrame(np.column_stack([kfold_treino]), 
					columns=['Soma', 'Media', 'Desvio Padrão', 'Min', 'Max'])
df.to_csv('DwtKF3.csv', encoding='utf-8', index=False)
kfold_teste[:1000] = images[iniBoa + 2000:iniBoa + 3000]
kfold_teste[1000:2000] = images[iniPonte + 2000:iniPonte + 3000]
kfold_teste[2000:3000] = images[iniAusente + 2000:iniAusente + 3000]
kfold_teste[3000:4000] = images[iniExcesso + 2000:iniExcesso + 3000]
kfold_teste[4000:5000] = images[iniPouca + 2000:iniPouca + 3000]

df = pd.DataFrame(np.column_stack([kfold_teste]), 
					columns=['Soma', 'Media', 'Desvio Padrão', 'Min', 'Max'])
df.to_csv('DwtKF3t.csv', encoding='utf-8', index=False)
kfold_treino[:3000] = images[iniBoa:iniBoa + 3000]
kfold_treino[3000:6000] = images[iniPonte:iniPonte + 3000]
kfold_treino[6000:9000] = images[iniAusente:iniAusente + 3000]
kfold_treino[9000:12000] = images[iniExcesso:iniExcesso + 3000]
kfold_treino[12000:15000] = images[iniPouca:iniPouca + 3000]

df = pd.DataFrame(np.column_stack([kfold_treino]), 
					columns=['Soma', 'Media', 'Desvio Padrão', 'Min', 'Max'])
df.to_csv('DwtKF4.csv', encoding='utf-8', index=False)
kfold_teste[:1000] = images[iniBoa + 3000:iniBoa + 4000]
kfold_teste[1000:2000] = images[iniPonte + 3000:iniPonte + 4000]
kfold_teste[2000:3000] = images[iniAusente + 3000:iniAusente + 4000]
kfold_teste[3000:4000] = images[iniExcesso + 3000:iniExcesso + 4000]
kfold_teste[4000:5000] = images[iniPouca + 3000:iniPouca + 4000]

df = pd.DataFrame(np.column_stack([kfold_teste]), 
					columns=['Soma', 'Media', 'Desvio Padrão', 'Min', 'Max'])
df.to_csv('DwtKF4t.csv', encoding='utf-8', index=False)
kfold_treino = np.zeros((20000,size_caracteristicas))
kfold_treino[:4000] = images[iniBoa:iniBoa + 4000]
kfold_treino[4000:8000] = images[iniPonte:iniPonte + 4000]
kfold_treino[8000:12000] = images[iniAusente:iniAusente + 4000]
kfold_treino[12000:16000] = images[iniExcesso:iniExcesso + 4000]
kfold_treino[16000:20000] = images[iniPouca:iniPouca + 4000]

df = pd.DataFrame(np.column_stack([kfold_treino]), 
					columns=['Soma', 'Media', 'Desvio Padrão', 'Min', 'Max'])
df.to_csv('DwtKFT.csv', encoding='utf-8', index=False)
kfold_teste = np.zeros((464*5,size_caracteristicas))
kfold_teste[:464] = images[iniBoa + 4000:iniPonte]
kfold_teste[464:2*464] = images[iniPonte + 4000:iniAusente]
kfold_teste[2*464:3*464] = images[iniAusente + 4000:iniExcesso]
kfold_teste[3*464:4*464] = images[iniExcesso + 4000:iniPouca]
kfold_teste[4*464:] = images[iniPouca + 4000:]

df = pd.DataFrame(np.column_stack([kfold_teste]), 
					columns=['Soma', 'Media', 'Desvio Padrão', 'Min', 'Max'])
df.to_csv('DwtKFTt.csv', encoding='utf-8', index=False)

# df.to_csv('Dwt.csv', encoding='utf-8', index=False)

print("FIM")

