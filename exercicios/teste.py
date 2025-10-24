import numpy as np
import cv2 as cv
import time
import os
imagesPath = 'images/'

def buscaImagens(filename: str) -> np.ndarray:
    fullPath = os.path.join(imagesPath, filename)
    
    if os.path.exists(fullPath):
        img = cv.imread(fullPath)
        if img is not None:
            return img
        else:
            print(f"Erro: Não foi possível carregar a imagem '{filename}'. O arquivo pode estar corrompido.")
    else:
        print(f"Erro: O arquivo '{filename}' não foi encontrado em '{imagesPath}'.")
    return np.array([])

def morfismo(imgInicial: np.typing.NDArray, imgFinal: np.typing.NDArray, peso: float) -> np.typing.NDArray:
    if not 0 <= peso <= 1:
        print('Peso deve estar entre 0 e 1!')
        return np.array([])
    return ((1-peso) * imgInicial + peso * imgFinal).astype(np.uint8)

img1 = buscaImagens('bowie1.jpg')
img2 = buscaImagens('bowie2.jpg')

windowName: str = 'teste'
cv.namedWindow(windowName)
i = 0
indo = True
while True:
    i = i + 1 if indo else i -1
    if i >= 60:
        indo = False
    if i<=0:
        indo = True
    peso: float = i / 60
    
    frameAtual: np.typing.NDArray = morfismo(img1, img2, peso)
    
    cv.imshow(windowName, frameAtual)

    key = cv.waitKey(17) 
    if key & 0xFF == ord('q'):
        print("Loop interrompido pelo usuário.")
        break
cv.destroyAllWindows()