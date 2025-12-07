import numpy as np
import cv2 as cv
import math
from matplotlib import pyplot as plt

def buscaImagem(filename: str) -> np.typing.NDArray:
    
    # if exists(filename):
    img = cv.imread(filename)
    #     if img is not None:
    #         return img
    #     else:
    #         print(f"Erro: Não foi possível carregar a imagem '{filename}'. O arquivo pode estar corrompido.")
    # else:
    #     print(f"Erro: O arquivo '{filename}' não foi encontrado!")

    assert img is not None, f'Nao foi possível encontrar a imagem {filename}'

    return np.array([])

def exibirImagens(imagens, titulos=None, colunas=3, figsize=(15, 5)):
    """
    Exibe uma lista de imagens em uma grade.
    
    Args:
        imagens: Lista de arrays (imagens).
        titulos: Lista opcional de strings para os títulos.
        colunas: Número de imagens por linha.
        figsize: Tupla definindo o tamanho da figura.
    """
    n_imagens = len(imagens)
    n_linhas = math.ceil(n_imagens / colunas)
    
    fig, ax = plt.subplots(n_linhas, colunas, figsize=figsize, squeeze=False)
    ax = ax.flatten()
    
    for i in range(len(ax)):
        if i < n_imagens:
            ax[i].imshow(imagens[i])
            ax[i].axis('off')

            if titulos and i < len(titulos):
                ax[i].set_title(titulos[i])
        else:
            ax[i].axis('off')
            
    plt.tight_layout()
    plt.show()