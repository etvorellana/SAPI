import pandas as pd
import cv2
import numpy as np
import imageio

from dwt_service import DwtService
#import os
#from PIL import Image

###Carrega as imagens

def carrega_img(pasta, lista, x): #Pasta de origem das imagens, lista que as imagens pertecem, numero de imagens
	for i in range(x):
		filename = (pasta + "/Solda_{}.png".format(i+1))
		lista.append(imageio.imread(filename))
	return lista

### Listas com as imagens
size_treinamento = 1000
size_caracteristicas = 5

images = np.zeros((size_treinamento, size_caracteristicas))

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

carrega_img('Soldas_boas', O_soldas_boas, 200)
carrega_img('Soldas_ponte', O_soldas_ponte, 200)
carrega_img('Soldas_ausente', O_soldas_ausente, 200)
carrega_img('Soldas_excesso', O_soldas_excesso, 200)
carrega_img('Soldas_pouca', O_soldas_pouca, 200)

#k = len(images)

#### Passa as imagens para escala de cinza

for i in range(200):
	O_soldas_boas[i] = cv2.cvtColor(O_soldas_boas[i], cv2.COLOR_BGR2GRAY)

for i in range(200):
	# O_soldas_boas[i] = cv2.cvtColor(O_soldas_boas[i], cv2.COLOR_BGR2GRAY)
	O_soldas_ponte[i] = cv2.cvtColor(O_soldas_ponte[i], cv2.COLOR_BGR2GRAY)
	O_soldas_ausente[i] = cv2.cvtColor(O_soldas_ausente[i], cv2.COLOR_BGR2GRAY)
	O_soldas_excesso[i] = cv2.cvtColor(O_soldas_excesso[i], cv2.COLOR_BGR2GRAY)
	O_soldas_pouca[i] = cv2.cvtColor(O_soldas_pouca[i], cv2.COLOR_BGR2GRAY)

dwtService = DwtService()
###########################################
####### Operações com as soldas boas ######
###########################################
for i in range(200):
	dwt_filtered_img = dwtService.dwt_filter(O_soldas_boas[i])
	lista_valores = dwtService.dwtSum(dwt_filtered_img)
	images[i] = lista_valores

##############################################
####### Operações com as soldas em ponte #####
##############################################
for i in range(200):
	dwt_filtered_img = dwtService.dwt_filter(O_soldas_ponte[i])
	lista_valores = dwtService.dwtSum(dwt_filtered_img)
	images[i + 200] = lista_valores

#############################################
####### Operações com as soldas ausente #####
#############################################
for i in range(200):
	dwt_filtered_img = dwtService.dwt_filter(O_soldas_ausente[i])
	lista_valores = dwtService.dwtSum(dwt_filtered_img)
	images[i + 400] = lista_valores

#############################################
####### Operações com as soldas excesso #####
#############################################
for i in range(200):
	dwt_filtered_img = dwtService.dwt_filter(O_soldas_excesso[i])
	lista_valores = dwtService.dwtSum(dwt_filtered_img)
	images[i + 600] = lista_valores

##########################################
####### Operações com as soldas pouca ####
##########################################
for i in range(200):
	dwt_filtered_img = dwtService.dwt_filter(O_soldas_pouca[i])
	lista_valores = dwtService.dwtSum(dwt_filtered_img)
	images[i + 800] = lista_valores


df = pd.DataFrame(np.column_stack([images]), columns=['Soma', 'Media', 'Desvio Padrão', 'Min', 'Max'])
#print(df.head(28))

df.to_csv('Dwt.csv', encoding='utf-8', index=False)

print("FIM")

