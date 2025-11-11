import heapq

def resolver_cenario3(nome_arquivo):
    # Carregar o grid do arquivo
    try:
        with open(nome_arquivo, 'r') as f:
            linhas = [linha.strip() for linha in f.readlines()]
    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
        return

    grid = [list(linha) for linha in linhas[1:]]
    if not grid:
        print("Erro: Grid vazio ou arquivo mal formatado.")
        return
        
    num_linhas = len(grid)
    num_colunas = len(grid[0])
    
    # Encontra as posições de início (S) e objetivo (G)
    inicio = None
    objetivo = None
    for r in range(num_linhas):
        for c in range(num_colunas):
            if grid[r][c] == 'S':
                inicio = (r, c)
            elif grid[r][c] == 'G':
                objetivo = (r, c)
    
    if not inicio or not objetivo:
        print("Erro: Posição de início 'S' ou objetivo 'G' não encontrada no grid.")
        return


    # Algoritmo de Dijkstra
    fila = [(0, inicio)]
    
    custos = { (r, c): float('inf') for r in range(num_linhas) for c in range(num_colunas) }
    custos[inicio] = 0
    
    predecessores = {}

    def obter_custo_movimento(celula):
        if celula in ['.', 'S', 'G']:
            return 1
        elif celula == '~':
            return 3
        return float('inf')

    # Movimentos possíveis: cima, baixo, esquerda, direita
    movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while fila:
        custo_atual, pos_atual = heapq.heappop(fila)

        if custo_atual > custos[pos_atual]:
            continue

        if pos_atual == objetivo:
            break

        r, c = pos_atual
        
        for dr, dc in movimentos:
            nova_r, nova_c = r + dr, c + dc

            if 0 <= nova_r < num_linhas and 0 <= nova_c < num_colunas:
                vizinho = (nova_r, nova_c)
                char_vizinho = grid[nova_r][nova_c]

                if char_vizinho == '#':
                    continue

                custo_mov = obter_custo_movimento(char_vizinho)
                novo_custo = custo_atual + custo_mov

                if novo_custo < custos[vizinho]:
                    custos[vizinho] = novo_custo
                    predecessores[vizinho] = pos_atual
                    heapq.heappush(fila, (novo_custo, vizinho))

    # Exibe o grid original
    print("Grid de entrada:")
    for linha in grid:
        print("".join(linha))
    print("\n\n---------------------------------------------------------------------\n\n")

    # Reconstrói e exibe o caminho
    if custos[objetivo] == float('inf'):
        print("Não foi possível encontrar um caminho de 'S' para 'G'.")
    else:
        print(f"Custo total do caminho: {custos[objetivo]}")
        
        caminho = []
        passo = objetivo
        while passo in predecessores:
            caminho.append(passo)
            passo = predecessores[passo]
        caminho.reverse()

        grid_resultado = [row[:] for row in grid]
        for r, c in caminho:
            if grid_resultado[r][c] not in ['S', 'G']:
                grid_resultado[r][c] = 'o'

        print("\nMapa com o caminho de menor custo:")
        for linha in grid_resultado:
            print("".join(linha))


if __name__ == '__main__':
    resolver_cenario3('../data/grid_example.txt')
