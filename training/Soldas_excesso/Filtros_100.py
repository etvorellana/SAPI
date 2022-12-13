import numpy as np
import cv2
import os
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
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        if value >= 0:
            lim = 255 - value
            v[v > lim] = 255
            v[v <= lim] += value
        else:
            lim = np.absolute(value)
            v[v < lim] = 0
            v[v >= lim] -= np.absolute(value)

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img
    
    elif cj_type == "s":
        # value = random.randint(-50, 50)
        value = np.random.choice(np.array([-50, -40, -30, 30, 40, 50]))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        if value >= 0:
            lim = 255 - value
            s[s > lim] = 255
            s[s <= lim] += value
        else:
            lim = np.absolute(value)
            s[s < lim] = 0
            s[s >= lim] -= np.absolute(value)

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
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
        image = cv2.add(image,gauss)
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


####IR até as 36

image = cv2.imread("Solda_1.png")

img_median = cv2.medianBlur(image, 3) # Add median filter to image
cv2.imwrite("Solda_8.png", img_median)

blur = cv2.blur(image,(3,3))
cv2.imwrite("Solda_9.png", img_median)

blur = cv2.blur(image,(5,5))
cv2.imwrite("Solda_10.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(3,3),0)
cv2.imwrite("Solda_11.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(5,5),0)
cv2.imwrite("Solda_12.png", gaussianBlur)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_13.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_14.png", brigh)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_16.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_17.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_18.png", sat)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_19.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_20.png", cons)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_21.png", gauss)

sp = noisy(image, "sp")
cv2.imwrite("Solda_15.png", sp)



######################################

image = cv2.imread("Solda_2.png")


img_median = cv2.medianBlur(image, 3) # Add median filter to image
cv2.imwrite("Solda_22.png", img_median)

blur = cv2.blur(image,(3,3))
cv2.imwrite("Solda_23.png", img_median)

blur = cv2.blur(image,(5,5))
cv2.imwrite("Solda_24.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(3,3),0)
cv2.imwrite("Solda_25.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(5,5),0)
cv2.imwrite("Solda_26.png", gaussianBlur)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_27.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_28.png", brigh)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_29.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_30.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_31.png", sat)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_32.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_33.png", cons)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_34.png", gauss)

sp = noisy(image, "sp")
cv2.imwrite("Solda_35.png", sp)

####################

image = cv2.imread("Solda_3.png")

img_median = cv2.medianBlur(image, 3) # Add median filter to image
cv2.imwrite("Solda_36.png", img_median)

blur = cv2.blur(image,(3,3))
cv2.imwrite("Solda_37.png", img_median)

blur = cv2.blur(image,(5,5))
cv2.imwrite("Solda_38.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(3,3),0)
cv2.imwrite("Solda_39.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(5,5),0)
cv2.imwrite("Solda_40.png", gaussianBlur)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_41.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_42.png", brigh)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_43.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_44.png", sat)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_45.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_46.png", cons)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_47.png", gauss)

sp = noisy(image, "sp")
cv2.imwrite("Solda_48.png", sp)


#########################################

image = cv2.imread("Solda_4.png")

img_median = cv2.medianBlur(image, 3) # Add median filter to image
cv2.imwrite("Solda_49.png", img_median)

blur = cv2.blur(image,(3,3))
cv2.imwrite("Solda_50.png", img_median)

blur = cv2.blur(image,(5,5))
cv2.imwrite("Solda_51.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(3,3),0)
cv2.imwrite("Solda_52.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(5,5),0)
cv2.imwrite("Solda_53.png", gaussianBlur)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_54.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_55.png", brigh)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_56.png", sat)


sat = colorjitter(image, "s")
cv2.imwrite("Solda_57.png", sat)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_58.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_59.png", cons)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_60.png", gauss)

sp = noisy(image, "sp")
cv2.imwrite("Solda_61.png", sp)

############################################

image = cv2.imread("Solda_5.png")

img_median = cv2.medianBlur(image, 3) # Add median filter to image
cv2.imwrite("Solda_62.png", img_median)

blur = cv2.blur(image,(3,3))
cv2.imwrite("Solda_63.png", img_median)

blur = cv2.blur(image,(5,5))
cv2.imwrite("Solda_64.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(3,3),0)
cv2.imwrite("Solda_65.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(5,5),0)
cv2.imwrite("Solda_66.png", gaussianBlur)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_67.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_68.png", brigh)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_69.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_70.png", sat)


cons = colorjitter(image, "c")
cv2.imwrite("Solda_71.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_72.png", cons)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_73.png", gauss)

sp = noisy(image, "sp")
cv2.imwrite("Solda_74.png", sp)


image = cv2.imread("Solda_6.png")

img_median = cv2.medianBlur(image, 3) # Add median filter to image
cv2.imwrite("Solda_75.png", img_median)

blur = cv2.blur(image,(3,3))
cv2.imwrite("Solda_76.png", img_median)

blur = cv2.blur(image,(5,5))
cv2.imwrite("Solda_77.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(3,3),0)
cv2.imwrite("Solda_78.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(5,5),0)
cv2.imwrite("Solda_79.png", gaussianBlur)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_80.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_81.png", brigh)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_82.png", sat)


sat = colorjitter(image, "s")
cv2.imwrite("Solda_83.png", sat)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_84.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_85.png", cons)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_86.png", gauss)

sp = noisy(image, "sp")
cv2.imwrite("Solda_87.png", sp)


image = cv2.imread("Solda_7.png")

img_median = cv2.medianBlur(image, 3) # Add median filter to image
cv2.imwrite("Solda_88.png", img_median)

blur = cv2.blur(image,(3,3))
cv2.imwrite("Solda_89.png", img_median)

blur = cv2.blur(image,(5,5))
cv2.imwrite("Solda_90.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(3,3),0)
cv2.imwrite("Solda_91.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(5,5),0)
cv2.imwrite("Solda_92.png", gaussianBlur)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_93.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_94.png", brigh)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_95.png", sat)


sat = colorjitter(image, "s")
cv2.imwrite("Solda_96.png", sat)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_97.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_98.png", cons)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_99.png", gauss)

sp = noisy(image, "sp")
cv2.imwrite("Solda_100.png", sp)

