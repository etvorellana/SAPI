import numpy as np
import cv2 as cv
import random

def colorjitter(img, cj_type):
    '''
    ### Different Color Jitter ###
    img: image
    cj_type: {b: brightness, s: saturation, c: constast}

    '''
    if cj_type == "b":
        # value = random.randint(-50, 50)
        value = np.random.choice(np.array([-50, -40, -30, 30, 40, 50]))
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        h, s, v = cv.split(hsv)
        if value >= 0:
            lim = 255 - value
            v[v > lim] = 255
            v[v <= lim] += value
        else:
            lim = np.absolute(value)
            v[v < lim] = 0
            v[v >= lim] -= np.absolute(value)

        final_hsv = cv.merge((h, s, v))
        img = cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)
        return img
    
    elif cj_type == "s":
        # value = random.randint(-50, 50)
        value = np.random.choice(np.array([-50, -40, -30, 30, 40, 50]))
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        h, s, v = cv.split(hsv)
        if value >= 0:
            lim = 255 - value
            s[s > lim] = 255
            s[s <= lim] += value
        else:
            lim = np.absolute(value)
            s[s < lim] = 0
            s[s >= lim] -= np.absolute(value)

        final_hsv = cv.merge((h, s, v))
        img = cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)
        return img
    
    elif cj_type == "c":
        brightness = 10
        contrast = random.randint(40, 100)
        dummy = np.int16(img)
        dummy = dummy * (contrast/127+1) - contrast + brightness
        dummy = np.clip(dummy, 0, 255)
        img = np.uint8(dummy)
        return img

def noisy(img, noise_type):
    '''
    ### Adding Noise ###
    img: image
    cj_type: {gauss: gaussian, sp: salt & pepper}
    '''
    if noise_type == "gauss":
        image=img.copy() 
        mean=0
        st=0.7
        gauss = np.random.normal(mean,st,image.shape)
        gauss = gauss.astype('uint8')
        image = cv.add(image,gauss)
        return image
    
    elif noise_type == "sp":
        image=img.copy() 
        prob = 0.05
        if len(image.shape) == 2:
            black = 0
            white = 255            
        else:
            colorspace = image.shape[2]
            if colorspace == 3:  # RGB
                black = np.array([0, 0, 0], dtype='uint8')
                white = np.array([255, 255, 255], dtype='uint8')
            else:  # RGBA
                black = np.array([0, 0, 0, 255], dtype='uint8')
                white = np.array([255, 255, 255, 255], dtype='uint8')
        probs = np.random.random(image.shape[:2])
        image[probs < (prob / 2)] = black
        image[probs > 1 - (prob / 2)] = white
        return image

def rotaImagem(imagem, nome = "Solda_", cont = 1):
    altura, largura = imagem.shape[:2]
    ponto = (largura / 2, altura / 2) #ponto no centro da figura
    rotaçoes = [30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]
    for ang in rotaçoes:
        print(ang)
        rotacao = cv.getRotationMatrix2D(ponto, ang, 1.0)
        rotImg = cv.warpAffine(imagem, rotacao, (largura, altura),
                                flags= cv.INTER_CUBIC,
                                borderMode=cv.BORDER_REPLICATE)
        cont += 1
        nameFile = nome + str(cont) + ".png"
        print(nameFile)
        cv.imwrite(nameFile, rotImg)

def aumentation(imagem, nome = "Solda_", cont = 1):
    
    img = cv.medianBlur(imagem, 3) # Add median filter to image
    cont += 1
    nameFile = nome + str(cont) + ".png"
    cv.imwrite(nameFile, img)

    img = cv.blur(imagem,(3,3))
    cont += 1
    nameFile = nome + str(cont) + ".png"
    cv.imwrite(nameFile, img)

    img = cv.blur(imagem,(5,5))
    cont += 1
    nameFile = nome + str(cont) + ".png"
    cv.imwrite(nameFile, img)

    img = cv.GaussianBlur(imagem,(3,3),0)
    cont += 1
    nameFile = nome + str(cont) + ".png"
    cv.imwrite(nameFile, img)

    img = cv.GaussianBlur(imagem,(5,5),0)
    cont += 1
    nameFile = nome + str(cont) + ".png"
    cv.imwrite(nameFile, img)

    for i in range(5):
        img = colorjitter(imagem, "b")
        cont += 1
        nameFile = nome + str(cont) + ".png"
        cv.imwrite(nameFile, img)
    
    for i in range(5):
        img = colorjitter(imagem, "s")
        cont += 1
        nameFile = nome + str(cont) + ".png"
        cv.imwrite(nameFile, img)

    for i in range(5):
        img = colorjitter(imagem, "c")
        cont += 1
        nameFile = nome + str(cont) + ".png"
        cv.imwrite(nameFile, img)

    for i in range(5):
        img = noisy(imagem, "gauss")
        cont += 1
        nameFile = nome + str(cont) + ".png"
        cv.imwrite(nameFile, img)

    for i in range(5):
        img = noisy(imagem, "sp")
        cont += 1
        nameFile = nome + str(cont) + ".png"
        cv.imwrite(nameFile, img)

    return cont

def main():
    imagem = cv.imread("Solda_1.png")
    print (imagem.shape)
    altura, largura = imagem.shape[:2]
    rotaImagem(imagem)
    transla = np.float32([[1, 0, 3],[0, 1, 0]])
    traImg = cv.warpAffine(imagem, transla, (largura, altura),
                        flags= cv.INTER_CUBIC,
                        borderMode=cv.BORDER_WRAP)
    cv.imwrite("Solda_17.png", traImg)
    rotaImagem(imagem, cont = 17)
    transla = np.float32([[1, 0, -3],[0, 1, 0]])
    traImg = cv.warpAffine(imagem, transla, (largura, altura),
                        flags= cv.INTER_CUBIC,
                        borderMode=cv.BORDER_WRAP)
    cv.imwrite("Solda_33.png", traImg)
    rotaImagem(traImg, cont = 33)
    transla = np.float32([[1, 0, 0],[0, 1, 3]])
    traImg = cv.warpAffine(imagem, transla, (largura, altura),
                        flags= cv.INTER_CUBIC,
                        borderMode=cv.BORDER_WRAP)
    cv.imwrite("Solda_49.png", traImg)
    rotaImagem(traImg, cont = 49)
    transla = np.float32([[1, 0, 0],[0, 1, -3]])
    traImg = cv.warpAffine(imagem, transla, (largura, altura),
                        flags= cv.INTER_CUBIC,
                        borderMode=cv.BORDER_WRAP)
    cv.imwrite("Solda_65.png", traImg)
    rotaImagem(traImg, cont = 65)
    transla = np.float32([[1, 0, 3],[0, 1, 3]])
    traImg = cv.warpAffine(imagem, transla, (largura, altura),
                        flags= cv.INTER_CUBIC,
                        borderMode=cv.BORDER_WRAP)
    cv.imwrite("Solda_81.png", traImg)
    rotaImagem(traImg, cont = 81)
    transla = np.float32([[1, 0, -3],[0, 1, 3]])
    traImg = cv.warpAffine(imagem, transla, (largura, altura),
                        flags= cv.INTER_CUBIC,
                        borderMode=cv.BORDER_WRAP)
    cv.imwrite("Solda_97.png", traImg)
    rotaImagem(traImg, cont = 97)
    transla = np.float32([[1, 0, 3],[0, 1, -3]])
    traImg = cv.warpAffine(imagem, transla, (largura, altura),
                        flags= cv.INTER_CUBIC,
                        borderMode=cv.BORDER_WRAP)
    cv.imwrite("Solda_113.png", traImg)
    rotaImagem(traImg, cont = 113)
    transla = np.float32([[1, 0, -3],[0, 1, -3]])
    traImg = cv.warpAffine(imagem, transla, (largura, altura),
                        flags= cv.INTER_CUBIC,
                        borderMode=cv.BORDER_WRAP)
    cv.imwrite("Solda_129.png", traImg)
    rotaImagem(traImg, cont = 129)
    j = 144
    for i in range(1,145):
        inFile = "Solda_" + str(i) + ".png"
        print(inFile)
        imagem = cv.imread(inFile)
        j = aumentation(imagem, cont = j)


if __name__ == "__main__":
    main()
