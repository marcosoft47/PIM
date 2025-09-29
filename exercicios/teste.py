import cv2 as cv

imgCinza = cv.imread('images/lenaShort.jpg', cv.IMREAD_GRAYSCALE)
imgColorida = cv.applyColorMap(imgCinza, cv.COLORMAP_PINK)

cv.imshow('Colorido', imgColorida)
cv.waitKey(0)

cv.destroyAllWindows()