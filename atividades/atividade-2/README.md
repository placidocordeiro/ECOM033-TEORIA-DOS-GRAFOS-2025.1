# Busca de Caminho com Grafos de Visibilidade e Árvores Geradoras Mínimas

## Visão Geral

Este projeto implementa um algoritmo de busca de caminho que combina grafos de visibilidade com o algoritmo de Árvore Geradora Mínima (AGM) de Kruskal e o algoritmo de caminho mais curto de Dijkstra. Encontra o caminho ótimo de um ponto inicial até um ponto objetivo, evitando obstáculos poligonais.

## Como Executar o Projeto

1. **Acesse o diretório raiz** do projeto:
   ```bash
   cd atividades/atividade-2
   ```

2. **Ative o ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/Mac
   venv\Scripts\activate       # Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o projeto**:
   ```bash
   python main.py
   ```

O programa lerá os dados de `input.txt`, gerará as visualizações e salvará os resultados nas pastas `plots/` e `data/`.

---

## Estrutura de Pastas

- **`data/`** → contém os grafos resultantes (em formato `.json`), como o grafo de visibilidade e o caminho mínimo.
- **`plots/`** → armazena as imagens geradas com as visualizações (grafo de visibilidade, AGM e caminho mínimo).

---

## Formato de Entrada

```
inicio_x, inicio_y
objetivo_x, objetivo_y
numero_de_obstaculos
quantidade_vertices_1
vertice_1_x, vertice_1_y
...
```
---

## Etapas do Algoritmo

### 1. Construção do Grafo de Visibilidade
Cria um grafo onde os vértices são o ponto inicial, o ponto objetivo e todos os vértices dos obstáculos. As arestas conectam vértices que têm linha de visão desobstruída.

![Grafo de Visibilidade](./plots/vis_graph.png)

### 2. Árvore Geradora Mínima (Algoritmo de Kruskal)
Reduz o grafo de visibilidade para sua árvore geradora mínima, mantendo apenas arestas essenciais enquanto preserva a conectividade.

![Grafo AGM](./plots/mst_graph.png)

### 3. Caminho Mais Curto (Algoritmo de Dijkstra)
Encontra o caminho de custo mínimo do início até o objetivo dentro da AGM usando o algoritmo de Dijkstra com fila de prioridade.

![Caminho Mínimo](./plots/minimum_path.png)

## Funções e Estruturas Principais

### `get_xy(fileline: str) -> tuple`
Lê uma linha de texto contendo duas coordenadas separadas por vírgula e retorna uma tupla `(x, y)` como `float`.  
Usada para converter o conteúdo de `input.txt` em pontos do plano.

---

### `read_input(input_path: str)`
Abre e interpreta o arquivo de entrada (`input.txt`), extraindo:
- Ponto inicial (`start`);
- Ponto objetivo (`goal`);
- Obstáculos (listas de vértices poligonais).  
Retorna uma tupla `(start, goal, obstacles)`.

---

### `create_visibility_graph(start, goal, obstacles)`
Constrói o **grafo de visibilidade**, conectando vértices que têm **linha de visão desobstruída**.  
Cada aresta recebe como peso a distância euclidiana entre os vértices.  
Retorna um grafo `networkx.Graph`.

---

### `class UnionFind`
Estrutura de dados para **detecção eficiente de ciclos** no algoritmo de Kruskal.  
Métodos principais:
- `make_set(x)` → inicializa um conjunto;
- `find(x)` → encontra o representante do conjunto;
- `union(x, y)` → une dois conjuntos distintos.

---

### `compute_mst_kruskal(graph)`
Implementa o algoritmo **Kruskal** para gerar a **Árvore Geradora Mínima (AGM)** do grafo.  
Utiliza `UnionFind` para evitar ciclos e retorna um grafo `mst` contendo as arestas mínimas que conectam todos os vértices.

---

### `dijkstra(mst: nx.Graph, start, goal)`
Executa o algoritmo **Dijkstra** sobre a árvore geradora mínima para encontrar o **caminho de menor custo** entre `start` e `goal`.  
Retorna:
- `path_graph` → grafo contendo apenas as arestas do caminho mínimo;
- `dist[goal]` → custo total do caminho.

---

### `draw_map(start, goal, obstacles, G, output_path, ...)`
Gera a **visualização gráfica** do ambiente, incluindo:
- Obstáculos poligonais;
- Ponto inicial e final;
- Arestas do grafo.  
O resultado é salvo em `plots/` com o título apropriado.

---

### `save_graph(graph, path)`
Serializa um grafo `networkx` em formato JSON, armazenando-o no diretório `data/`.

---

### `main()`
Ponto de entrada do progrma que coordena toda a execução:
1. Lê os dados de entrada;
2. Cria o grafo de visibilidade;
3. Gera e salva a AGM via Kruskal;
4. Executa Dijkstra para obter o caminho mínimo;
5. Gera as visualizações e salva os resultados.

---

## Componentes Principais

- **Grafo de Visibilidade**: Conecta todos os pares de vértices visíveis
- **Union-Find**: Detecção eficiente de ciclos para o algoritmo de Kruskal
- **Algoritmo de Dijkstra**: Computa caminho mais curto com fila de prioridade
- **Visualização**: Renderização de caminho baseada em Matplotlib

## Saídas

- `plots/vis_graph.png` - Visualização do grafo de visibilidade
- `plots/mst_graph.png` - Árvore geradora mínima
- `plots/minimum_path.png` - Caminho ótimo final
- `data/grafo.json` - Estrutura do grafo
- `data/dijkstra_path.json` - Dados do caminho
