import numpy as np
import cv2 as cv
from os.path import exists

def buscaImagem(filename: str) -> np.typing.NDArray:
    
    if exists(filename):
        img = cv.imread(filename)
        if img is not None:
            return img
        else:
            print(f"Erro: Não foi possível carregar a imagem '{filename}'. O arquivo pode estar corrompido.")
    else:
        print(f"Erro: O arquivo '{filename}' não foi encontrado!")

    # assert img is not None, 'não leu a imagem'

    return np.array([])