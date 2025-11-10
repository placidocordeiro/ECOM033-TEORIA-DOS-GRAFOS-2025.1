# Cenário 3

## Pseudocódigo

```
Início
    d₁₁ ← 0; d₁ᵢ ← ∞ ∀ i ∈ V - {1};   [origem-origem zero; distâncias infinitas a partir da origem]
    A ← V; F ← Ø; anterior (i) ← 0 ∀ i;
    enquanto A ≠ Ø fazer
        Início
            r ← v ∈ V | d₁ᵣ = min[d₁ⱼ]      [acha o vértice mais próximo da origem]
                                  j∈A

            F ← F ∪ {r}; A ← A - {r};       [o vértice r sai de Aberto para Fechado]
            S ← A ∩ N⁺(r)                   [S são os sucessores de r ainda abertos]
            para todo i ∈ S fazer
                Início
                    p ← min [d₁ᵢᵏ⁻¹, (d₁ᵣ + vᵣᵢ)]   [compara o valor anterior com a nova soma]

                    se p < d₁ᵢᵏ⁻¹ então
                        Início
                            d₁ᵢᵏ ← p; anterior (i) ← r;   [ganhou a nova distância!]
                        fim;
                fim;
        fim;
fim.
```

## Algorítmo aplicado

```
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
```

## Análise comparativa

| Conceito no algoritmo de Dijkstra | Pseudocódigo | Código Python |
| :--- | :--- | :--- |
| **Inicialização** | `d₁₁ ← 0; d₁ᵢ ← ∞ ∀ i ∈ V - {1};` (Define a distância da origem como 0 e todas as outras como infinito) <br> `A ← V;` (Conjunto `A` contém todos os vértices a serem visitados) | `custos = { (r, c): float('inf') ... }` <br> `custos[inicio] = 0` (Um dicionário `custos` armazena as distâncias, inicializadas como infinito, exceto para o início) |
| **Estrutura de dados principal** | `enquanto A ≠ Ø fazer` (O loop continua enquanto houver vértices "abertos" para visitar) | `fila = [(0, inicio)]` <br> `while fila:` (Usa uma fila de prioridade (min-heap) para determinar o próximo vértice a visitar. O loop continua enquanto a fila não estiver vazia) |
| **Seleção do próximo vértice** | `r ← v ∈ V | d₁ᵣ = min[d₁ⱼ]` (Encontra o vértice `r` no conjunto `A` com a menor distância `d`) | `custo_atual, pos_atual = heapq.heappop(fila)` (A biblioteca `heapq` remove e retorna eficientemente o item com a menor prioridade - neste caso, o menor custo - da fila) |
| **Atualização dos vértices "fechados"** | `F ← F ∪ {r}; A ← A - {r};` (Move o vértice `r` do conjunto "aberto" (`A`) para o "fechado" (`F`)) | Esta parte é implícita no Python. Uma vez que um nó é extraído da fila de prioridade (`heappop`) e processado, ele não é adicionado de volta com o mesmo estado. A verificação `if custo_atual > custos[pos_atual]: continue` garante que apenas os caminhos mais curtos sejam processados. |
| **Exploração dos vizinhos** | `para todo i ∈ S fazer` (Onde `S` são os sucessores/vizinhos de `r` que ainda estão em `A`) | `for dr, dc in movimentos:` <br> `if 0 <= nova_r < num_linhas and 0 <= nova_c < num_colunas:` (Itera sobre os vizinhos válidos da posição atual) |
| **Relaxamento da aresta** | `se p < d₁ᵢᵏ⁻¹ então d₁ᵢᵏ ← p; anterior (i) ← r;` (Se um caminho mais curto para o vizinho `i` for encontrado através de `r`, atualiza a distância e o predecessor) | `if novo_custo < custos[vizinho]:` <br> `custos[vizinho] = novo_custo` <br> `predecessores[vizinho] = pos_atual` <br> `heapq.heappush(fila, (novo_custo, vizinho))` (Se um custo menor for encontrado, ele é atualizado, o predecessor é registrado e o vizinho é adicionado à fila de prioridade com o novo custo) |
