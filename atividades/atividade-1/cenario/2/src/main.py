import math
import sys
from typing import List, Tuple, Optional

GRAPH_PATH = '../data/graph2.txt'
SOURCE = 0
DEST = 6

def read_graph(path: str) -> Tuple[int, List[Tuple[int,int,float]]]:
    edges: List[Tuple[int,int,float]] = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            tokens = []
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split()
                tokens.extend(parts)
            V = int(tokens[0])
            E = int(tokens[1])
            idx = 2
            for _ in range(E):
                u = int(tokens[idx]); v = int(tokens[idx+1]); w = float(tokens[idx+2])
                edges.append((u, v, w))
                idx += 3
            return V, edges
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    except Exception:
        raise

def bellman_ford(V: int, edges: List[Tuple[int,int,float]], source: int):
    dist = [math.inf] * V
    pred: List[Optional[int]] = [None] * V
    dist[source] = 0.0

    for iteration in range(V - 1):
        updated = False
        for (u, v, w) in edges:
            if dist[u] != math.inf and dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                pred[v] = u
                updated = True
        if not updated:
            break

    neg_cycle = False
    for (u, v, w) in edges:
        if dist[u] != math.inf and dist[v] > dist[u] + w:
            neg_cycle = True
            break

    return dist, pred, neg_cycle

def reconstruct_path(pred: List[Optional[int]], source: int, dest: int) -> Optional[List[int]]:
    if dest < 0 or dest >= len(pred):
        return None
    path = []
    cur = dest
    if pred[cur] is None and cur != source:
        if cur == source:
            return [source]
        return None
    while cur is not None:
        path.append(cur)
        if cur == source:
            break
        cur = pred[cur]
    path.reverse()
    if path and path[0] == source:
        return path
    return None

def main(path=GRAPH_PATH, source=SOURCE, dest=DEST):
    try:
        V, edges = read_graph(path)
    except Exception as e:
        print("Erro ao ler o grafo:", e)
        return

    if source < 0 or source >= V or dest < 0 or dest >= V:
        print(f"Vértice source ({source}) ou dest ({dest}) fora do intervalo 0..{V-1}.")
        return

    dist, pred, neg_cycle = bellman_ford(V, edges, source)

    if neg_cycle:
        print("ATENÇÃO: ciclo de custo negativo detectado (distâncias podem não ser bem definidas).")

    path_list = reconstruct_path(pred, source, dest)
    if path_list is None:
        print(f"Destino {dest} não é alcançável a partir de {source}.")
    else:
        total_cost = dist[dest]
        path_str = " -> ".join(map(str, path_list))
        print("Caminho mínimo (origem -> destino):", path_str)
        print("Somatório do custo do caminho (Wh):", int(total_cost))

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) >= 3:
        GRAPH_PATH = args[0]
        SOURCE = int(args[1])
        DEST = int(args[2])
    elif len(args) == 1:
        GRAPH_PATH = args[0]
    main(GRAPH_PATH, SOURCE, DEST)
