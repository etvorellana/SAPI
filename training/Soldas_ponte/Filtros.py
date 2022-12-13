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

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_15.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_16.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_17.png", brigh)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_18.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_19.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_20.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_21.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_22.png", sat)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_23.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_24.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_25.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_26.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_27.png", cons)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_28.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_29.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_30.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_31.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_32.png", gauss)

sp = noisy(image, "sp")
cv2.imwrite("Solda_33.png", sp)

sp = noisy(image, "sp")
cv2.imwrite("Solda_34.png", sp)

sp = noisy(image, "sp")
cv2.imwrite("Solda_35.png", sp)


######################################

image = cv2.imread("Solda_2.png")

img_median = cv2.medianBlur(image, 3) # Add median filter to image
cv2.imwrite("Solda_37.png", img_median)

blur = cv2.blur(image,(3,3))
cv2.imwrite("Solda_38.png", img_median)

blur = cv2.blur(image,(5,5))
cv2.imwrite("Solda_39.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(3,3),0)
cv2.imwrite("Solda_40.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(5,5),0)
cv2.imwrite("Solda_41.png", gaussianBlur)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_42.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_43.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_44.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_45.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_46.png", brigh)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_47.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_48.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_49.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_50.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_51.png", sat)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_52.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_53.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_54.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_55.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_56.png", cons)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_57.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_58.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_59.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_60.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_61.png", gauss)

sp = noisy(image, "sp")
cv2.imwrite("Solda_62.png", sp)

sp = noisy(image, "sp")
cv2.imwrite("Solda_63.png", sp)

sp = noisy(image, "sp")
cv2.imwrite("Solda_64.png", sp)

sp = noisy(image, "sp")
cv2.imwrite("Solda_65.png", sp)

####################

image = cv2.imread("Solda_3.png")
img_median = cv2.medianBlur(image, 3) # Add median filter to image
cv2.imwrite("Solda_66.png", img_median)

blur = cv2.blur(image,(3,3))
cv2.imwrite("Solda_67.png", img_median)

blur = cv2.blur(image,(5,5))
cv2.imwrite("Solda_68.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(3,3),0)
cv2.imwrite("Solda_69.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(5,5),0)
cv2.imwrite("Solda_70.png", gaussianBlur)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_71.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_72.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_73.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_74.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_75.png", brigh)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_76.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_77.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_78.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_79.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_80.png", sat)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_81.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_82.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_83.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_84.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_85.png", cons)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_86.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_87.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_88.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_89.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_90.png", gauss)

sp = noisy(image, "sp")
cv2.imwrite("Solda_91.png", sp)

sp = noisy(image, "sp")
cv2.imwrite("Solda_92.png", sp)

sp = noisy(image, "sp")
cv2.imwrite("Solda_93.png", sp)


#########################################

image = cv2.imread("Solda_4.png")
img_median = cv2.medianBlur(image, 3) # Add median filter to image
cv2.imwrite("Solda_94.png", img_median)

blur = cv2.blur(image,(3,3))
cv2.imwrite("Solda_95.png", img_median)

blur = cv2.blur(image,(5,5))
cv2.imwrite("Solda_96.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(3,3),0)
cv2.imwrite("Solda_97.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(5,5),0)
cv2.imwrite("Solda_98.png", gaussianBlur)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_99.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_100.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_101.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_102.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_104.png", brigh)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_105.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_106.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_107.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_108.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_109.png", sat)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_110.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_111.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_112.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_113.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_114.png", cons)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_115.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_116.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_117.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_118.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_119.png", gauss)

sp = noisy(image, "sp")
cv2.imwrite("Solda_120.png", sp)

sp = noisy(image, "sp")
cv2.imwrite("Solda_121.png", sp)

sp = noisy(image, "sp")
cv2.imwrite("Solda_103.png", sp)


############################################

image = cv2.imread("Solda_5.png")
img_median = cv2.medianBlur(image, 3) # Add median filter to image
cv2.imwrite("Solda_124.png", img_median)

blur = cv2.blur(image,(3,3))
cv2.imwrite("Solda_125.png", img_median)

blur = cv2.blur(image,(5,5))
cv2.imwrite("Solda_126.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(3,3),0)
cv2.imwrite("Solda_127.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(5,5),0)
cv2.imwrite("Solda_128.png", gaussianBlur)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_129.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_130.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_131.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_132.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_133.png", brigh)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_134.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_135.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_136.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_137.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_138.png", sat)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_139.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_140.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_141.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_142.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_143.png", cons)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_144.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_145.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_146.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_147.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_148.png", gauss)

sp = noisy(image, "sp")
cv2.imwrite("Solda_122.png", sp)

sp = noisy(image, "sp")
cv2.imwrite("Solda_123.png", sp)



image = cv2.imread("Solda_6.png")
img_median = cv2.medianBlur(image, 3) # Add median filter to image
cv2.imwrite("Solda_153.png", img_median)

blur = cv2.blur(image,(3,3))
cv2.imwrite("Solda_154.png", img_median)

blur = cv2.blur(image,(5,5))
cv2.imwrite("Solda_155.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(3,3),0)
cv2.imwrite("Solda_156.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(5,5),0)
cv2.imwrite("Solda_157.png", gaussianBlur)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_158.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_159.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_160.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_161.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_162.png", brigh)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_163.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_164.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_165.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_166.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_167.png", sat)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_168.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_169.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_170.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_171.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_172.png", cons)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_173.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_174.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_175.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_149.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_150.png", gauss)

sp = noisy(image, "sp")
cv2.imwrite("Solda_151.png", sp)

sp = noisy(image, "sp")
cv2.imwrite("Solda_152.png", sp)


image = cv2.imread("Solda_7.png")
img_median = cv2.medianBlur(image, 3) # Add median filter to image
cv2.imwrite("Solda_182.png", img_median)

blur = cv2.blur(image,(3,3))
cv2.imwrite("Solda_183.png", img_median)

blur = cv2.blur(image,(5,5))
cv2.imwrite("Solda_184.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(3,3),0)
cv2.imwrite("Solda_185.png", blur)

gaussianBlur = cv2.GaussianBlur(image,(5,5),0)
cv2.imwrite("Solda_186.png", gaussianBlur)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_187.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_188.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_189.png", brigh)

brigh = colorjitter(image, "b")
cv2.imwrite("Solda_190.png", brigh)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_191.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_192.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_193.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_181.png", sat)

sat = colorjitter(image, "s")
cv2.imwrite("Solda_194.png", sat)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_195.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_196.png", cons)



cons = colorjitter(image, "c")
cv2.imwrite("Solda_197.png", cons)

cons = colorjitter(image, "c")
cv2.imwrite("Solda_198.png", cons)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_199.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_200.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_176.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_177.png", gauss)

gauss = noisy(image, "gauss")
cv2.imwrite("Solda_178.png", gauss)

sp = noisy(image, "sp")
cv2.imwrite("Solda_179.png", sp)

sp = noisy(image, "sp")
cv2.imwrite("Solda_180.png", sp)

