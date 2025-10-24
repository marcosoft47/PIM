import pickle
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import csv

def contarAglomerados3D(matriz: np.typing.NDArray, valoresAlvo: list[int], conectividade: int, verboso=False) -> dict[int, int]:
    """
    Contar aglomerados 3D usando um algoritmo de busca (BFS).
    """

    def _obterVizinhos(voxel: tuple[int, int, int], shape: tuple[int, int, int], conectividade: int) -> list[tuple[int, int, int]]:
        """
        Função auxiliar para encontrar os vizinhos de um voxel com base na conectividade.
        """
        z, y, x = voxel
        dim_z, dim_y, dim_x = shape
        vizinhos = []

        # Define os deslocamentos para cada tipo de conectividade
        # d(z, y, x)
        if conectividade == 6:
            offsets = [
                (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)
            ]
        elif conectividade == 18:
            offsets = []
            for dz in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if abs(dz) + abs(dy) + abs(dx) in [1, 2]: # Face ou Aresta
                            offsets.append((dz, dy, dx))
        elif conectividade == 26:
            offsets = []
            for dz in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if not (dz == 0 and dy == 0 and dx == 0): # Todos menos o centro
                            offsets.append((dz, dy, dx))
        
        for dz, dy, dx in offsets:
            novo_z, novo_y, novo_x = z + dz, y + dy, x + dx
            # Verifica se o vizinho está dentro dos limites da matriz
            if 0 <= novo_z < dim_z and 0 <= novo_y < dim_y and 0 <= novo_x < dim_x:
                vizinhos.append((novo_z, novo_y, novo_x))
                
        return vizinhos

    def _bfs(pontoPartida: tuple[int, int, int], mascara: np.typing.NDArray, visitados: np.typing.NDArray, conectividade: int):
        """
        Função auxiliar que executa a Busca em Largura (BFS) para "inundar" um aglomerado.
        """
        fila = deque([pontoPartida])
        # print(fila)
        visitados[pontoPartida] = True
        contador = 0
        
        while fila:
            voxelAtual = fila.popleft()
            
            vizinhos = _obterVizinhos(voxelAtual, mascara.shape, conectividade)
            
            for vizinho in vizinhos:
                # Se o vizinho tem o valor que queremos E ainda não foi visitado
                if mascara[vizinho] and not visitados[vizinho]:
                    visitados[vizinho] = True
                    fila.append(vizinho)
                    contador += 1
        print(contador)
    
    if conectividade not in [6, 18, 26]:
        raise ValueError("A conectividade deve ser 6, 18 ou 26.")
        
    resultados = {}
    dim_z, dim_y, dim_x = matriz.shape
    
    for valor in valoresAlvo:
        # Cria a máscara binária para o valor alvo
        mascaraValor = (matriz == valor)
        visitados = np.zeros_like(mascaraValor, dtype=bool)
        contadorAglomerados = 0
        
        # Itera por cada voxel da matriz
        for z in range(dim_z):
            for y in range(dim_y):
                for x in range(dim_x):
                    # Se encontramos um voxel do valor alvo que ainda não foi visitado
                    if mascaraValor[z, y, x] and not visitados[z, y, x]:
                        # Achamos um novo aglomerado!
                        contadorAglomerados += 1
                        # Inicia a "inundação" para marcar todos os seus membros como visitados
                        _bfs((z, y, x), mascaraValor, visitados, conectividade)
        
        resultados[valor] = contadorAglomerados
    
    if verboso:
        print(
            # f"Necróticas: {resultados[140]}\n"\
            f"Quiescente: {resultados[200]}\n"\
            # f"Proliferativas: {resultados[255]}"
        )

    return resultados


def obterTamanhosDosAglomerados(matriz: np.typing.NDArray, valoresAlvo: list[int], conectividade: int, verboso=False) -> dict[int, list[int]]:
    """
    Encontrar os tamanhos de todos os aglomerados 3D.
    """
    def _obterVizinhos(voxel: tuple[int, int, int], shape: tuple[int, int, int], conectividade: int) -> list[tuple[int, int, int]]:
        """
        Encontra os vizinhos de um voxel com base na conectividade.
        """
        z, y, x = voxel
        dim_z, dim_y, dim_x = shape
        vizinhos = []

        if conectividade == 6:
            offsets = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        elif conectividade == 18:
            offsets = [(dz, dy, dx) for dz in [-1, 0, 1] for dy in [-1, 0, 1] for dx in [-1, 0, 1] if abs(dz) + abs(dy) + abs(dx) in [1, 2]]
        elif conectividade == 26:
            offsets = [(dz, dy, dx) for dz in [-1, 0, 1] for dy in [-1, 0, 1] for dx in [-1, 0, 1] if not (dz == 0 and dy == 0 and dx == 0)]
        
        for dz, dy, dx in offsets:
            novo_z, novo_y, novo_x = z + dz, y + dy, x + dx
            if 0 <= novo_z < dim_z and 0 <= novo_y < dim_y and 0 <= novo_x < dim_x:
                vizinhos.append((novo_z, novo_y, novo_x))
                
        return vizinhos

    def _bfs_com_contagem(pontoPartida: tuple[int, int, int], mascara: np.typing.NDArray, visitados: np.typing.NDArray, conectividade: int) -> int:
        """
        Executa a Busca em Largura (BFS) para "inundar" um aglomerado E CONTA SEU TAMANHO.
        """
        fila = deque([pontoPartida])
        visitados[pontoPartida] = True
        tamanho_cluster = 1  # Começa a contagem com 1 (o ponto de partida)
        
        while fila:
            voxelAtual = fila.popleft()
            
            for vizinho in _obterVizinhos(voxelAtual, mascara.shape, conectividade):
                if mascara[vizinho] and not visitados[vizinho]:
                    visitados[vizinho] = True
                    tamanho_cluster += 1 # Incrementa o contador para cada novo voxel encontrado
                    fila.append(vizinho)
                    
        return tamanho_cluster

    if conectividade not in [6, 18, 26]:
        raise ValueError("A conectividade deve ser 6, 18 ou 26.")
        
    resultados = {}
    dim_z, dim_y, dim_x = matriz.shape
    
    for valor in valoresAlvo:
        mascaraValor = (matriz == valor)
        visitados = np.zeros_like(mascaraValor, dtype=bool)
        lista_de_tamanhos = []
        
        for z in range(dim_z):
            for y in range(dim_y):
                for x in range(dim_x):
                    if mascaraValor[z, y, x] and not visitados[z, y, x]:
                        # Encontrou um novo aglomerado. Inicia a busca para contar seu tamanho.
                        tamanho_do_cluster = _bfs_com_contagem((z, y, x), mascaraValor, visitados, conectividade)
                        lista_de_tamanhos.append(tamanho_do_cluster)
        
        resultados[valor] = lista_de_tamanhos 
    if verboso:
        print(
        f"Necróticas: {resultados[140]}\n\n"\
        f"Quiescente: {resultados[200]}\n\n"\
        f"Proliferativas: {resultados[255]}"
        )
        
    return resultados

def plot(data:np.typing.NDArray):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    mapeamento_celulas = {
    140: ('black', 'Necróticas'),
    200: ('gray', 'Quiescente'),
    255: ('red', 'Proliferativas')
    }
    for valor, (cor, rotulo) in mapeamento_celulas.items():
    # np.where é a forma mais eficiente de encontrar as coordenadas
    # Retorna uma tupla de 3 arrays: (array_de_Zs, array_de_Ys, array_de_Xs)
        coords_z, coords_y, coords_x = np.where(data == valor)
        
        # Plotar os pontos no gráfico de dispersão
        ax.scatter(coords_x, coords_y, coords_z, c=cor, label=rotulo, marker='o', s=15) # type: ignore

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()

def hist(data6:list[int], data26:list[int]):
    fig, axs = plt.subplots(1,2, tight_layout=True)

    uniq6=np.unique(data6, return_counts=True)
    uniq26=np.unique(data26, return_counts=True)
    axs[0].hist(data6, label='Conectividade-6', bins=len(uniq6[0]))
    axs[1].hist(data26, label='Conectividade-26', bins=len(uniq26[0]))
    print()
    print()
    plt.show()

def countCells(file: np.typing.NDArray):
    return np.unique(file, return_counts=True)

def getDict(data: tuple, verboso=False):
    dictionary = {
        'Necróticas': 0,
        'Quiescentes': 0,
        'Proliferativas': 0
    }
    for i in range(len(data[0])):
        match data[0][i]:
            case 140:
                dictionary['Necróticas'] = data[1][i]
            case 200:
                dictionary['Quiescentes'] = data[1][i]
            case 255:
                dictionary['Proliferativas'] = data[1][i]
    if verboso:
        print(f"Necróticas: {dictionary['Necróticas']}\nQuiescente: {dictionary['Quiescentes']}\nProliferativas: {dictionary['Proliferativas']}")
    return dictionary



with open("volume_TAC", "rb") as file:
    with open('resultados.csv', mode='w') as csv_file:
        try:
            img: np.typing.NDArray = pickle.load(file)
            writer = csv.writer(csv_file)
            # print('Total de voxels:')
            # getDict(countCells(img), verboso=True)
            # print('\nAglomerados:')
            print('Conectividade-6:')
            # contarAglomerados3D(img,[140,200,255], 6, verboso=True)
            res6 = obterTamanhosDosAglomerados(img, [140,200,255], 6)
            print(countCells(np.array(res6[140])))
            print(countCells(np.array(res6[200])))
            print(countCells(np.array(res6[255])))
            # res6[140].sort()
            # res6[200].sort()
            # res6[255].sort()
            # print('\nConectividade-18:')
            # contarAglomerados3D(img,[140,200,255], 18, verboso=True)
            print('\nConectividade-26:')
            # contarAglomerados3D(img,[140,200,255], 26, verboso=True)
            res26 = obterTamanhosDosAglomerados(img, [140,200,255], 26)
            print(countCells(np.array(res26[140])))
            print(countCells(np.array(res26[200])))
            print(countCells(np.array(res26[255])))
            # res26[140].sort()
            # res26[200].sort()
            # res26[255].sort()
            # writer.writerow(res6[140])
            # writer.writerow(res6[200])
            # writer.writerow(res6[255])
            # writer.writerow(res26[140])
            # writer.writerow(res26[200])
            # writer.writerow(res26[255])
            # plot(img)
            # showImage(img)
        except EOFError:
            pass

