## Como executar

Ao clonar o repositório, execute os seguintes comandos na raiz do projeto

```bash
cd ./cenario/1/src
python main.py
```

## Pseudocódigo (base teórica)

O pseudocódigo fornecido descreve o funcionamento clássico do algoritmo de Floyd-Warshall:

```text
início <dados G = (V,E); matriz de valores V(G); matriz de roteamento R = [r_ij];
r_ij ← j    ∀i;
D⁰ ← [d_ij] ← V(G);

para k = 1, ..., n fazer [k é o vértice-base da iteração]
    início
        para todo i, j = 1, ..., n fazer
            se d_ik + d_kj < d_ij então
                início
                    d_ij ← d_ik + d_kj
                    r_ij ← r_ik
                fim
        fim
    fim
fim.
```

### Estrutura do pseudocódigo

1. **Entrada do grafo** → vértices `V`, arestas `E`.
2. **Construção da matriz de valores** `V(G)` e da matriz de roteamento `R`.
3. **Inicialização** → `r_ij ← j` e `D⁰ ← V(G)`.
4. **Laços principais** → três laços aninhados (`k`, `i`, `j`).
5. **Relaxamento** → condição `d_ik + d_kj < d_ij` e atualização das matrizes.

---

## Implementação em Python

### 1. Representação das arestas

```python
class Edge:
    def __init__(self, origin: int, destiny: int, cost: int):
        self.origin = origin
        self.destiny = destiny
        self.cost = cost
```

**Equivalente ao pseudocódigo:** definição de `E` (conjunto de arestas).

---

### 2. Inicialização da matriz de distâncias

```python
def init_matrix(n):
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(0)
            else:
                row.append(inf)
        matrix.append(row)
    return matrix
```

**Equivalente a:**

* Construção de `D⁰ ← [d_ij]`.
* Aqui, a diagonal é inicializada com `0` (`d_ii = 0`) e os demais com `∞`.

---

### 3. Construção da matriz de valores `V(G)`

```python
def build_value_matrix(matrix, lst_edges: list[Edge]):
    for edge in lst_edges:
        matrix[edge.origin-1][edge.destiny-1] = edge.cost
    return matrix
```

**Equivalente a:**

* Preenchimento da matriz `V(G)` com os custos das arestas.

Observação: o pseudocódigo também considera a **matriz de roteamento** `R = [r_ij]`, mas essa parte não foi implementada no Python.

---

### 4. Algoritmo Floyd-Warshall

```python
def floyd(num_vertex: int, num_edges: int, lst_edges: list[Edge]):
    matrix = init_matrix(num_vertex)
    vm = build_value_matrix(matrix, lst_edges)

    for k in range(num_vertex):               # laço k = 1..n
        for i in range(num_vertex):           # laço i = 1..n
            for j in range(num_vertex):       # laço j = 1..n
                if vm[i][k] + vm[k][j] < vm[i][j]:   # se d_ik + d_kj < d_ij
                    vm[i][j] = vm[i][k] + vm[k][j]   # d_ij ← d_ik + d_kj
    return vm
```

**Equivalente a:**

* O trecho corresponde diretamente ao loop `para k`, `para i`, `para j`.
* Implementa a verificação e atualização das distâncias (`d_ij`).
* **Diferença**: não existe atualização da matriz de roteamento `R` (`r_ij ← r_ik`), presente no pseudocódigo.

---

### 5. Identificação do vértice central

```python
def find_central_node(value_matrix, num_vertex):
    central_node = None
    minimum_cost = inf
    central_ad_list = []

    for i in range(num_vertex):
        current_cost = 0
        current_ad_list = []

        for j in range(num_vertex):
            current_cost = current_cost + value_matrix[i][j]
            current_ad_list.append(value_matrix[i][j])

        if current_cost < minimum_cost:
            central_node = i
            minimum_cost = current_cost
            central_ad_list = current_ad_list

    return central_node, central_ad_list
```

**Extensão além do pseudocódigo:**

* Essa função não aparece no pseudocódigo.
* Foi criada para **resolver o problema da estação central**, escolhendo o vértice cuja soma das distâncias é mínima.

---

### 6. Entrada e execução

```python
with open("../data/graph1.txt") as f:
    num_vertex, num_edges = [int(x) for x in f.readline().split()]
    for _ in range(num_edges):
        u, v, cost = [int(x) for x in f.readline().split()]
        edge = Edge(u, v, cost)
        lst_edges.append(edge)
```

**Equivalente a:**

* Entrada dos dados `G = (V, E)`.
* Lido a partir de arquivo ao invés de fornecido diretamente.

---