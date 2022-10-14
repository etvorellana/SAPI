import numpy as np
from csv import reader
from random import shuffle
from scipy.spatial.distance import cdist


def mahalanobis(data, x):
    m = np.mean(data, axis = 0)
    #print("mean: ", m)

    xMm = x - m
    #print("The difference  with mean xMm: ",xMm)

    data = np.transpose(data)
    covM = np.cov(data, bias = False)
    invCoveM = np.linalg.inv(covM)

    np.set_printoptions(suppress=True)
    #print("Covariance matrix of data:\n", covM)
    #print("Inv Covariance matrix of data:\n", invCoveM)

    tem1 = np.dot(xMm, invCoveM)
    tem2 = np.dot(tem1, np.transpose(xMm))
    #print(tem1)
    #print(tem2)
    MD = np.sqrt(tem2)

    #print("The Mahalanobis distance: ", np.reshape(MD, -1))

    result = np.reshape(MD, -1)
    return result

def calculo(confirmar, l_teste,l_treinamento_boa, l_treinamento_pouca, l_treinamento_ponte, l_treinamento_excesso, l_treinamento_ausente):
    MR = np.zeros((5, 5), dtype=int)
    classificacao = []
    classe = ['Boa', 'Ponte', 'Ausente', 'Excesso', 'Pouca']
    for i in range(200):
        result1 = mahalanobis(l_treinamento_boa, l_teste[i])
        #print("Dist. solda boa: ", result1)
        classificacao.append(result1)
        result2 = mahalanobis(l_treinamento_ponte, l_teste[i])
        #print("Dist. solda em ponte: ", result2)
        classificacao.append(result2)
        result3 = mahalanobis(l_treinamento_ausente, l_teste[i])
        #print("Dist. solda ausente: ", result3)
        classificacao.append(result3)
        result4 = mahalanobis(l_treinamento_excesso, l_teste[i])
        #print("Dist. solda em excesso: ", result4)
        classificacao.append(result4)
        result5 = mahalanobis(l_treinamento_pouca, l_teste[i])
        #print("Dist. Pouca solda: ", result5)
        classificacao.append(result5)
        
        #confirmar = l_teste_aux[i][4]
        #print(confirmar)
        aux = classificacao.index(min(classificacao))
        #print ("Previsão do algoritimo: ", classe[aux], "e a classe correta é: ", classe[confirmar[i]])
        MR[confirmar[i]][aux]+=1
        classificacao.clear()
    return MR

def kfold (lista_soldas, k):
    l_teste = []
    l_treinamento = []

    auxiliar = [ ]

    for i in range(1000):
        auxiliar.append(lista_soldas[i][8])

    print("\n----K = ", k,"-------")
    if k == 1:
        l_teste = lista_soldas[0:200].copy()
        print("Tamanho da lista de teste: ", len(l_teste))
        l_treinamento = lista_soldas[200:1000].copy()
        print("Tamanho da lista de treinamento: ", len(l_treinamento))

    elif k == 2:
        l_teste = lista_soldas[200:400].copy()
        print("Tamanho da lista de teste: ", len(l_teste))
        for i in range (200):
            l_treinamento.append(lista_soldas[i])
        for i in range (400, 1000):
            l_treinamento.append(lista_soldas[i])
        print("Tamanho da lista de treinamento: ", len(l_treinamento))

    elif k == 3:
        l_teste = lista_soldas[400:600].copy()
        print("Tamanho da lista de teste: ", len(l_teste))
        for i in range (400):
            l_treinamento.append(lista_soldas[i])
        for i in range (600, 1000):
            l_treinamento.append(lista_soldas[i])
        print("Tamanho da lista de treinamento: ", len(l_treinamento))

    elif k == 4:
        l_teste = lista_soldas[600:800].copy()
        print("Tamanho da lista de teste: ", len(l_teste))
        for i in range (600):
            l_treinamento.append(lista_soldas[i])
        for i in range (800,1000):
            l_treinamento.append(lista_soldas[i])
        print("Tamanho da lista de treinamento: ", len(l_treinamento))

    else:
        l_teste = lista_soldas[800:1000].copy()
        print("Tamanho da lista de teste: ", len(l_teste))
        for i in range (800):
            l_treinamento.append(lista_soldas[i])
        print("Tamanho da lista de treinamento: ", len(l_treinamento))

    confirmar = []
    solda_boa = 0
    solda_ponte = 0
    solda_ausente = 0
    solda_excesso = 0
    solda_pouca = 0

    x = len(l_teste)
    for i in range(x):
        n = l_teste[i][8]
        confirmar.append(int(n))
        del (l_teste[i][8])
        if n == 0:
            solda_boa += 1
        elif n == 1:
            solda_ponte += 1
        elif n == 2:
            solda_ausente += 1
        elif n == 3:
            solda_excesso += 1
        else:
            solda_pouca += 1

    print("\n---Quantidade de cada classe de solda no conjunto de teste:---")
    print("Solda boa: ", solda_boa)
    print("Solda ponte: ", solda_ponte)
    print("Solda ausente: ", solda_ausente)
    print("Solda excesso: ", solda_excesso)
    print("Solda pouca: ", solda_pouca)

    l_treinamento_boa = []
    l_treinamento_ponte = []
    l_treinamento_ausente = []
    l_treinamento_excesso = []
    l_treinamento_pouca = []

    x = len(l_treinamento)
    for i in range(x):
        n = l_treinamento[i][8]
        del (l_treinamento[i][8])
        if n == 0:
            l_treinamento_boa.append(l_treinamento[i])
        elif n == 1:
            l_treinamento_ponte.append(l_treinamento[i])
        elif n == 2:
            l_treinamento_ausente.append(l_treinamento[i])
        elif n == 3:
            l_treinamento_excesso.append(l_treinamento[i])
        else:
            l_treinamento_pouca.append(l_treinamento[i])

    print("\n---Tamanho do conjunto de treinamento de cada classe---")
    print("Solda boa: ", len(l_treinamento_boa))
    print("Solda ponte: ", len(l_treinamento_ponte))
    print("Solda ausente: ", len(l_treinamento_ausente))
    print("Solda excesso: ", len(l_treinamento_excesso))
    print("Solda pouca: ", len(l_treinamento_pouca))

    MR = calculo(confirmar, l_teste,l_treinamento_boa, l_treinamento_pouca, l_treinamento_ponte, l_treinamento_excesso, l_treinamento_ausente)
    l_teste.clear()
    l_treinamento.clear()
    l_treinamento_boa.clear()
    l_treinamento_ponte.clear()
    l_treinamento_ausente.clear()
    l_treinamento_excesso.clear()
    l_treinamento_pouca.clear()
    print("Matriz de resultado:")
    print(MR)
    for x in range(1000):
        lista_soldas[x].append(auxiliar[x])              
    return MR

#print(lista_soldas[2])
#print("---------------")

lista_soldas = []

with open('Gabor_1k.csv', 'r') as csv_file:
    csv_reader = reader(csv_file)
    lista_soldas = list(csv_reader)
    #print(lista_soldas)


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

#Coloando em ordem aleatória
shuffle(lista_soldas)
#print(lista_soldas[0])
teste1 = kfold(lista_soldas, 1)
#print(lista_soldas[1])
teste2 = kfold(lista_soldas, 2)
teste3 = kfold(lista_soldas, 3)
teste4 = kfold(lista_soldas, 4)
teste5 = kfold(lista_soldas, 5)

MRF = MR = np.zeros((5, 5), dtype=float)


for x in range(1):
    for y in range(5):
        MRF[x][y] = (teste1[x][y]+teste2[x][y]+teste3[x][y]+teste4[x][y]+teste5[x][y])/200

for x in range(1,5):
    for y in range(5):
        MRF[x][y] = (teste1[x][y]+teste2[x][y]+teste3[x][y]+teste4[x][y]+teste5[x][y])/200

print("Resutaldo Final: ")
print(MRF)





