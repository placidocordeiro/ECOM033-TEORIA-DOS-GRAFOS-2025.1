from shapely.geometry import Point, LineString, Polygon
from itertools import combinations
import networkx as nx
import math
from matplotlib.patches import Polygon as MplPolygon
import json
import os
import matplotlib.pyplot as plt
import heapq
import numpy as np

PLOT_PATH = "./plots/"
DATA_PATH = "./data"

def get_xy(fileline: str) -> tuple:
    if not fileline or not fileline.strip():
        raise ValueError("Linha vazia ao ler coordenada.")
    parts = [p.strip() for p in fileline.strip().split(',')]
    if len(parts) != 2:
        raise ValueError("Formato inválido de coordenada.")
    return float(parts[0]), float(parts[1])

def read_input(input_path: str):
    try:
        with open(input_path) as f:
            start = get_xy(f.readline())
            goal = get_xy(f.readline())
            num_obs = int(f.readline())
            obstacles = [ [get_xy(f.readline()) for _ in range(int(f.readline()))] for _ in range(num_obs) ]
    except FileNotFoundError:
        print("Arquivo de entrada não encontrado. Certifique-se de que o arquivo existe.")
        raise
    except Exception as e:
        print(f"Algo de errado aconteceu. {e}")
        raise
    return start, goal, obstacles    

def create_visibility_graph(start, goal, obstacles):
    G = nx.Graph()
    vertices = [start, goal] + [v for obs in obstacles for v in obs]
    polygons = [Polygon(obs) for obs in obstacles]

    for v in vertices:
        G.add_node(v, pos=v)

    for v1, v2 in combinations(vertices, 2):
        line = LineString([v1, v2])
        is_visible = all(not (line.crosses(poly) or line.within(poly)) for poly in polygons)
        if is_visible:
            dist = math.hypot(v2[0]-v1[0], v2[1]-v1[1])
            G.add_edge(v1, v2, weight=dist)
    
    return G

class UnionFind:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def make_set(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        xroot = self.find(x)
        yroot = self.find(y)
        if xroot == yroot:
            return False
        if self.rank[xroot] < self.rank[yroot]:
            self.parent[xroot] = yroot
        elif self.rank[yroot] < self.rank[xroot]:
            self.parent[yroot] = xroot
        else:
            self.parent[yroot] = xroot
            self.rank[xroot] += 1
        return True

def compute_mst_kruskal(graph):
    mst = nx.Graph()
    for n, data in graph.nodes(data=True):
        mst.add_node(n, **data)

    uf = UnionFind()
    for n in graph.nodes():
        uf.make_set(n)

    edges = []
    for u, v, attr in graph.edges(data=True):
        w = attr.get('weight', None)
        if w is None:
            w = float('inf')
        edges.append( (w, u, v) )

    edges.sort(key=lambda x: x[0])

    for w, u, v in edges:
        if uf.find(u) != uf.find(v):
            merged = uf.union(u, v)
            if merged:
                mst.add_edge(u, v, weight=w)

    return mst

def dijkstra(mst: nx.Graph, start, goal):
    dist = {node: math.inf for node in mst.nodes()}
    dist[start] = 0

    prev = {node: None for node in mst.nodes()}

    pq = [(0, start)]

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        if current_node == goal:
            break

        if current_dist > dist[current_node]:
            continue

        for neighbor in mst.neighbors(current_node):
            weight = mst[current_node][neighbor]['weight']
            new_dist = current_dist + weight

            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = current_node
                heapq.heappush(pq, (new_dist, neighbor))
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()

    path_graph = nx.Graph()
    for i in range(len(path)-1):
        u = path[i]
        v = path[i+1]
        path_graph.add_edge(u, v, weight=mst[u][v]['weight'])

    return path_graph, dist[goal]

def draw_map(start, goal, obstacles, G, output_path, figsize=(8, 8), padding=5.0, title=None):
    fig, ax = plt.subplots(figsize=figsize)

    for obs in obstacles:
        poly_patch = MplPolygon(obs, closed=True, facecolor='lightgray', edgecolor='black', alpha=0.7)
        ax.add_patch(poly_patch)
        xs, ys = zip(*obs + [obs[0]])
        ax.plot(xs, ys, color='black', linewidth=1)

    ax.plot(start[0], start[1], marker='o', color='green', markersize=8, label='start')
    ax.plot(goal[0], goal[1], marker='x', color='red', markersize=8, label='goal')

    xs = [start[0], goal[0]] + [x for obs in obstacles for x, _ in obs]
    ys = [start[1], goal[1]] + [y for obs in obstacles for _, y in obs]

    ax.set_xlim(min(xs) - padding, max(xs) + padding)
    ax.set_ylim(min(ys) - padding, max(ys) + padding)
    ax.set_aspect('equal', 'box')
    ax.grid(True)
    ax.legend()

    for edge in G.edges(data=True):
        v1, v2, weight = edge
        ax.plot([v1[0], v2[0]], [v1[1], v2[1]], color='#FF0000', linewidth=1, alpha=0.5)
        
    if title is not None:
        ax.set_title(title)
    
    fig.savefig(output_path, bbox_inches='tight', dpi=250)
    plt.show()

def save_graph(graph, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = nx.node_link_data(graph, edges="links")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    try:
        start, goal, obstacles = read_input('input.txt')
        G = create_visibility_graph(start, goal, obstacles)

        print("======== EXIBINDO START E GOAL ========")
        print(f"{start}, {goal}")
        print()

        print("======== EXIBINDO OBSTÁCULOS ========")
        for obs in obstacles:
            print(obs)
        print()
        
        print("PLOTANDO GRÁFICO DE VISIBILIDADE (plots/vis_grapsh)")
        plot_file = "vis_graph.png"
        draw_map(start, goal, obstacles, G, PLOT_PATH + plot_file)

        print("SALVANDO GRAFO DE VISIBILIDADE (data/grafo.json)...")
        os.makedirs('data', exist_ok=True)
        save_graph(G, 'data/grafo.json')

        print("CALCULANDO ÁRVORE GERADORA MÍNIMA (MST) VIA KRUSKAL")
        mst = compute_mst_kruskal(G)
        print("ÁRVORE GERADORA MÍNIMA ENCONTRADA COM SUCESSO!!")
        
        print("PLOTANDO ÁRVORE GERADORA MÍNIMA....")
        plot_file = "mst_graph"
        draw_map(start, goal, obstacles, mst, PLOT_PATH + plot_file)
        
        print("EXECUTANDO DIJKSTRA PARA ENCONTRAR O CAMINHO MÍNIMO")
        minimum_path, cost = dijkstra(mst, start, goal)
        print("CAMINHO MÍNIMO ENCONTRADO COM SUCESSO!!")
        save_graph(minimum_path, DATA_PATH + "diskstra_path.png")
        
        # ========== DEBUG ===============
    
        print("custo:", cost, type(cost))
        print("nós do path_graph:", list(minimum_path.nodes()))
        print("arestas do path_graph:", list(minimum_path.edges(data=True)))
        # se seus nós são tuplas (x,y), mostre tipos e valores
        for n in minimum_path.nodes():
            print("node:", n, "type:", type(n))
            if isinstance(n, tuple):
                print("  elems types:", [type(e) for e in n])
        
        print("PLOTANDO CAMINHO MÍNIMO...")
        title = f"Custo mínimo encontrado: {cost}"
        file_path = PLOT_PATH + "minimum_path.png"
        draw_map(start, goal, obstacles, minimum_path, file_path, title)
        
    except Exception as e:
        print("Erro ao desenhar mapa:", e)

if __name__ == "__main__":
    main()
