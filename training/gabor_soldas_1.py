import pandas as pd
import cv2
import numpy as np
from skimage.filters import gabor_kernel
import imageio
#import os
#from PIL import Image


###CRIAÇÃO DOS KERNELS PARA OS FILTROS
theta_init = 0
freq_init = 0.1
sigmax_init = 3
sigmay_init = 3

nucleo1 = np.real(gabor_kernel(0.1, 0,sigma_x=sigmax_init, sigma_y=sigmay_init))
nucleo2 = np.real(gabor_kernel(0.3, 0,sigma_x=sigmax_init, sigma_y=sigmay_init))
nucleo3 = np.real(gabor_kernel(0.1, np.pi/4,sigma_x=sigmax_init, sigma_y=sigmay_init))
nucleo4 = np.real(gabor_kernel(0.3, np.pi/4,sigma_x=sigmax_init, sigma_y=sigmay_init))


###Carrega as imagens

def carrega_img(pasta, lista, x): #Pasta de origem das imagens, lista que as imagens pertecem, numero de imagens
	for i in range(x):
		filename = (pasta + "/Solda_{}.png".format(i+1))
		lista.append(imageio.imread(filename))
	return lista


### Listas com as imagens

#images = []

L_soma = []
L_media = [ ]
L_desvio = [ ]
L_classe = [ ]

L_soma_k1 = []
L_desvio_k1 = [ ]

L_soma_k2 = []
L_desvio_k2 = [ ]

L_soma_k3 = []
L_desvio_k3 = [ ]

L_soma_k4 = []
L_desvio_k4 = [ ]

fimg = []
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
	L_classe.append(0)
	

for i in range(200):
	#O_soldas_boas[i] = cv2.cvtColor(O_soldas_boas[i], cv2.COLOR_BGR2GRAY)
	O_soldas_ponte[i] = cv2.cvtColor(O_soldas_ponte[i], cv2.COLOR_BGR2GRAY)
	O_soldas_ausente[i] = cv2.cvtColor(O_soldas_ausente[i], cv2.COLOR_BGR2GRAY)
	O_soldas_excesso[i] = cv2.cvtColor(O_soldas_excesso[i], cv2.COLOR_BGR2GRAY)
	O_soldas_pouca[i] = cv2.cvtColor(O_soldas_pouca[i], cv2.COLOR_BGR2GRAY)

for i in range(200):
	L_classe.append(1)

for i in range(200):
	L_classe.append(2)

for i in range(200):
	L_classe.append(3)

for i in range(200):
	L_classe.append(4)


###########################################
####### Operações com as soldas boas ######
###########################################
for i in range(200):
	L_soma_k1.append(np.sum(cv2.filter2D(O_soldas_boas[i], cv2.CV_8UC3, nucleo1)))
	L_desvio_k1.append(np.std(cv2.filter2D(O_soldas_boas[i], cv2.CV_8UC3, nucleo1)))

	L_soma_k2.append(np.sum(cv2.filter2D(O_soldas_boas[i], cv2.CV_8UC3, nucleo2)))
	L_desvio_k2.append(np.std(cv2.filter2D(O_soldas_boas[i], cv2.CV_8UC3, nucleo2)))

	L_soma_k3.append(np.sum(cv2.filter2D(O_soldas_boas[i], cv2.CV_8UC3, nucleo3)))
	L_desvio_k3.append(np.std(cv2.filter2D(O_soldas_boas[i], cv2.CV_8UC3, nucleo3)))

	L_soma_k4.append(np.sum(cv2.filter2D(O_soldas_boas[i], cv2.CV_8UC3, nucleo4)))
	L_desvio_k4.append(np.std(cv2.filter2D(O_soldas_boas[i], cv2.CV_8UC3, nucleo4)))


##############################################
####### Operações com as soldas em ponte #####
##############################################
for i in range(200):
	L_soma_k1.append(np.sum(cv2.filter2D(O_soldas_ponte[i], cv2.CV_8UC3, nucleo1)))
	L_desvio_k1.append(np.std(cv2.filter2D(O_soldas_ponte[i], cv2.CV_8UC3, nucleo1)))

	L_soma_k2.append(np.sum(cv2.filter2D(O_soldas_ponte[i], cv2.CV_8UC3, nucleo2)))
	L_desvio_k2.append(np.std(cv2.filter2D(O_soldas_ponte[i], cv2.CV_8UC3, nucleo2)))

	L_soma_k3.append(np.sum(cv2.filter2D(O_soldas_ponte[i], cv2.CV_8UC3, nucleo3)))
	L_desvio_k3.append(np.std(cv2.filter2D(O_soldas_ponte[i], cv2.CV_8UC3, nucleo3)))

	L_soma_k4.append(np.sum(cv2.filter2D(O_soldas_ponte[i], cv2.CV_8UC3, nucleo4)))
	L_desvio_k4.append(np.std(cv2.filter2D(O_soldas_ponte[i], cv2.CV_8UC3, nucleo4)))

#############################################
####### Operações com as soldas ausente #####
#############################################
for i in range(200):
	L_soma_k1.append(np.sum(cv2.filter2D(O_soldas_ausente[i], cv2.CV_8UC3, nucleo1)))
	L_desvio_k1.append(np.std(cv2.filter2D(O_soldas_ausente[i], cv2.CV_8UC3, nucleo1)))

	L_soma_k2.append(np.sum(cv2.filter2D(O_soldas_ausente[i], cv2.CV_8UC3, nucleo2)))
	L_desvio_k2.append(np.std(cv2.filter2D(O_soldas_ausente[i], cv2.CV_8UC3, nucleo2)))

	L_soma_k3.append(np.sum(cv2.filter2D(O_soldas_ausente[i], cv2.CV_8UC3, nucleo3)))
	L_desvio_k3.append(np.std(cv2.filter2D(O_soldas_ausente[i], cv2.CV_8UC3, nucleo3)))

	L_soma_k4.append(np.sum(cv2.filter2D(O_soldas_ausente[i], cv2.CV_8UC3, nucleo4)))
	L_desvio_k4.append(np.std(cv2.filter2D(O_soldas_ausente[i], cv2.CV_8UC3, nucleo4)))

#############################################
####### Operações com as soldas excesso #####
#############################################
for i in range(200):
	L_soma_k1.append(np.sum(cv2.filter2D(O_soldas_excesso[i], cv2.CV_8UC3, nucleo1)))
	L_desvio_k1.append(np.std(cv2.filter2D(O_soldas_excesso[i], cv2.CV_8UC3, nucleo1)))

	L_soma_k2.append(np.sum(cv2.filter2D(O_soldas_excesso[i], cv2.CV_8UC3, nucleo2)))
	L_desvio_k2.append(np.std(cv2.filter2D(O_soldas_excesso[i], cv2.CV_8UC3, nucleo2)))

	L_soma_k3.append(np.sum(cv2.filter2D(O_soldas_excesso[i], cv2.CV_8UC3, nucleo3)))
	L_desvio_k3.append(np.std(cv2.filter2D(O_soldas_excesso[i], cv2.CV_8UC3, nucleo3)))

	L_soma_k4.append(np.sum(cv2.filter2D(O_soldas_excesso[i], cv2.CV_8UC3, nucleo4)))
	L_desvio_k4.append(np.std(cv2.filter2D(O_soldas_excesso[i], cv2.CV_8UC3, nucleo4)))

##########################################
####### Operações com as soldas pouca ####
##########################################
for i in range(200):
	L_soma_k1.append(np.sum(cv2.filter2D(O_soldas_pouca[i], cv2.CV_8UC3, nucleo1)))
	L_desvio_k1.append(np.std(cv2.filter2D(O_soldas_pouca[i], cv2.CV_8UC3, nucleo1)))

	L_soma_k2.append(np.sum(cv2.filter2D(O_soldas_pouca[i], cv2.CV_8UC3, nucleo2)))
	L_desvio_k2.append(np.std(cv2.filter2D(O_soldas_pouca[i], cv2.CV_8UC3, nucleo2)))

	L_soma_k3.append(np.sum(cv2.filter2D(O_soldas_pouca[i], cv2.CV_8UC3, nucleo3)))
	L_desvio_k3.append(np.std(cv2.filter2D(O_soldas_pouca[i], cv2.CV_8UC3, nucleo3)))

	L_soma_k4.append(np.sum(cv2.filter2D(O_soldas_pouca[i], cv2.CV_8UC3, nucleo4)))
	L_desvio_k4.append(np.std(cv2.filter2D(O_soldas_pouca[i], cv2.CV_8UC3, nucleo4)))


df = pd.DataFrame(np.column_stack([L_soma_k1, L_desvio_k1, L_soma_k2, L_desvio_k2, L_soma_k3, L_desvio_k3, L_soma_k4, L_desvio_k4, L_classe]), columns=['Soma k1', 'Desvio Padrão k1', 'Soma k2', 'Desvio Padrão k2', 'Soma k3', 'Desvio Padrão k3', 'Soma k4', 'Desvio Padrão k4', 'Classe'])
#print(df.head(28))

df.to_csv('Gabor_1_2k.csv', encoding='utf-8', index=False)

#print("FIM")

