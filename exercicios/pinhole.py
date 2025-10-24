import numpy as np

def projecao_cartesiana(pontos3d: np.ndarray, distanciaFocal: float) -> np.ndarray:
    ''' Faz a projeção do objeto real numa imagem em sistema cartesiano'''
    # Separação das colunas
    colX = pontos3d[:, 0]
    colY = pontos3d[:, 1]
    colZ = pontos3d[:, 2]

    # Normalização
    zNorm = colZ / distanciaFocal
    xNorm = colX / zNorm
    yNorm = colY / zNorm
    return np.column_stack([xNorm, yNorm])

def projecao_pixel(pontos3d: np.ndarray, distanciaFocal: float, tamanhoSensor: float) -> np.ndarray:
    ''' Faz a projeção do objeto real numa imagem em pixels '''
    mm = projecao_cartesiana(pontos3d, distanciaFocal)
    return (mm / tamanhoSensor).astype(int)

coordenadas = np.array(
    [[650.7, 2000, 1500],
     [653.5, 2000, 1500],
     [650.7, 1990, 1500],
     [653.5, 1990, 1500],
     [645.3, 500.3, 1500],
     [645, 500.3, 1500],
     [645.3, 500, 1500],
     [645, 500, 1500]]
)

# test = np.array([
#     [0,         2000,	1500],
#     [1304.2,	2000,	1500],
#     [1304.2,	0,	    1500],
#     [0,     	0,	    1500]
# ])

print(projecao_pixel(coordenadas, 5, 0.00042))
# [[ 5164 15873]
#  [ 5186 15873]
#  [ 5164 15793]
#  [ 5186 15793]
#  [ 5121  3970]
#  [ 5119  3970]
#  [ 5121  3968]
#  [ 5119  3968]]

print(projecao_pixel(coordenadas, 5, 0.085))
# [[25 78]
#  [25 78]
#  [25 78]
#  [25 78]
#  [25 19]
#  [25 19]
#  [25 19]
#  [25 19]]
 