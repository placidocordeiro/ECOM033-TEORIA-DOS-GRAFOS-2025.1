from shapely.geometry import Point, LineString, Polygon
from itertools import combinations
import networkx as nx
import math
from matplotlib.patches import Polygon as MplPolygon
import json
import os
import matplotlib.pyplot as plt

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

    for v1, v2 in combinations(vertices, 2):
        line = LineString([v1, v2])
        is_visible = all(not (line.crosses(poly) or line.within(poly)) for poly in polygons)
        if is_visible:
            dist = math.sqrt((v2[0]-v1[0])**2 + (v2[1]-v1[1])**2)
            G.add_edge(v1, v2, weight=dist)
    
    return G

def draw_map(start, goal, obstacles, G, figsize=(8, 8), padding=5.0):
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
        ax.plot([v1[0], v2[0]], [v1[1], v2[1]], color='blue', linewidth=1, alpha=0.5)

    plt.show()

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

        print("SALVANDO GRAFO...")
        json_data = nx.node_link_data(G, edges="edges")
        os.makedirs('data', exist_ok=True)
        with open('data/grafo.json', 'w') as f:
            json.dump(json_data, f, indent=2)

        draw_map(start, goal, obstacles, G)

    except Exception as e:
        print("Erro ao desenhar mapa:", e)

if __name__ == "__main__":
    main()
