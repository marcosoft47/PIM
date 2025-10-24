import cv2 as cv
import numpy as np
bayer = np.array(
        [[10,130,15,110],
         [215,40,250,30],
         [15,255,15,255],
         [210,30,255,45]],
         dtype=np.uint8)
img = cv.cvtColor(bayer, cv.COLOR_BAYER_RG2BGR)
imgCinza = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
print(imgCinza)

l1 = int(input('Informe o limite inferior: '))
l2 = int(input('Informe o limite superior: '))
(l1, l2) = (l1, l2) if l1 < l2 else (l2, l1)

threshold = cv.inRange(imgCinza, l1, l2) #type: ignore
# threshold = cv.inRange(imgCinza, np.array([l1]), np.array([l2])) # Se o Pylance reclamar da resposta de cima
cv.imshow('Threshold', threshold)
cv.waitKey()
# thresholdNumpy = np.where(l1 < imgCinza < l2, [0,0,0], [255,255,255])
# print(thresholdNumpy)