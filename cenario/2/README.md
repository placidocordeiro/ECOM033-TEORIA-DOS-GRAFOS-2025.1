# 1. Objetivo

Este script implementa o algoritmo **Bellman–Ford** para encontrar o caminho mínimo entre dois vértices em um grafo direcionado, permitindo pesos negativos — como no cenário do problema proposto (carro elétrico com regeneração).

A entrada é um arquivo de texto (`graph2.txt`) contendo:

```
<num_vertices> <num_arestas>
<vertice_inicial> <vertice_final> <custo>
...
```

A saída é:

* Caminho mínimo entre `SOURCE` e `DEST`
* Custo total desse caminho (Wh)
* Aviso de ciclo negativo se houver

---

## 2. Como executar

Ao clonar o diretório, execute os seguintes comandos na raiz:

```bash
cd ./cenario/2/src
python main.py
```

## 3. Estrutura do Pseudocódigo Bellman–Ford

O pseudocódigo clássico segue geralmente esta lógica:

```
1. Inicializar:
   para cada vértice v:
       d[v] = ∞
       pred[v] = null
   d[source] = 0

2. Repetir |V|-1 vezes:
   para cada aresta (u, v) com peso w:
       se d[v] > d[u] + w então:
           d[v] = d[u] + w
           pred[v] = u

3. Detectar ciclos negativos:
   para cada aresta (u, v) com peso w:
       se d[v] > d[u] + w então:
           ciclo negativo detectado

4. Reconstruir caminho:
   partir de dest, seguir pred[v] até source
```

---

## 4. Comparação Linha a Linha

### **Configuração inicial**

```python
GRAPH_PATH = '../data/graph2.txt'
SOURCE = 0
DEST = 6
```

**Equivale à escolha de parâmetros do problema** — define caminho do grafo, vértice inicial (source) e final (destino).

---

### **Função `read_graph`**

```python
def read_graph(path: str) -> Tuple[int, List[Tuple[int,int,float]]]:
```

**Não existe no pseudocódigo clássico** — é um pré-processamento para ler dados do arquivo e transformar em lista de arestas.
Corresponde à **leitura da entrada do problema**.

Dentro dessa função:

```python
V = int(tokens[0])
E = int(tokens[1])
```

Pseudocódigo: leitura de `|V|` e `|E|`.

```python
edges.append((u, v, w))
```

Cria a lista de arestas `(u,v,w)` para uso no algoritmo.

---

### **Função `bellman_ford`**

```python
dist = [math.inf] * V
pred: List[Optional[int]] = [None] * V
dist[source] = 0.0
```

**Passo 1 do pseudocódigo**: inicialização

* `dist` = vetor `d[]` → inicializado com infinito
* `pred` = vetor `pred[]` (predecessores)
* `dist[source] = 0` → distância inicial da fonte é zero

---

#### Loop principal — Relaxamento das arestas

```python
for iteration in range(V - 1):
    updated = False
    for (u, v, w) in edges:
        if dist[u] != math.inf and dist[v] > dist[u] + w:
            dist[v] = dist[u] + w
            pred[v] = u
            updated = True
    if not updated:
        break
```

**Passo 2 do pseudocódigo**

* O loop externo roda `|V|-1` vezes (propriedade do Bellman–Ford).
* O loop interno percorre todas as arestas `(u,v,w)`.
* A condição `dist[v] > dist[u] + w` é a condição de relaxamento.
* `dist[v] = dist[u] + w` → atualização da distância mínima.
* `pred[v] = u` → registro do predecessor.
* O `updated` é um otimização extra: se nenhuma atualização ocorrer, interrompe mais cedo (corresponde ao “enquanto existe relaxamento” do pseudocódigo otimizado).

---

#### Detecção de ciclos negativos

```python
neg_cycle = False
for (u, v, w) in edges:
    if dist[u] != math.inf and dist[v] > dist[u] + w:
        neg_cycle = True
        break
```

**Passo 3 do pseudocódigo**
Após `|V|-1` iterações, se ainda houver relaxamento possível → ciclo negativo detectado.

---

### **Função `reconstruct_path`**

```python
def reconstruct_path(pred: List[Optional[int]], source: int, dest: int) -> Optional[List[int]]:
```

**Passo 4 do pseudocódigo**

* Reconstrói o caminho mínimo partindo do destino e seguindo o vetor `pred[]` até a fonte.
* Se não existir caminho válido → retorna `None`.

---

### **Função `main`**

```python
V, edges = read_graph(path)
dist, pred, neg_cycle = bellman_ford(V, edges, source)
path_list = reconstruct_path(pred, source, dest)
```

Conjunto de chamadas correspondentes aos passos do pseudocódigo.

Depois:

```python
if neg_cycle:
    print("ATENÇÃO: ciclo de custo negativo detectado")
```

Output conforme passo 3 do pseudocódigo.

```python
path_str = " -> ".join(map(str, path_list))
print("Caminho mínimo:", path_str)
print("Somatório do custo:", int(total_cost))
```

Saída final: caminho mínimo e custo total.

---

### **Bloco `if __name__ == "__main__":**

```python
args = sys.argv[1:]
```

Não faz parte do pseudocódigo clássico — serve para receber parâmetros de linha de comando, aumentando a flexibilidade do script.

---
