from math import inf

class Edge:
    def __init__(self, origin: int, destiny: int, cost: int):
        self.origin = origin
        self.destiny = destiny
        self.cost = cost

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

def build_value_matrix(matrix, lst_edges: list[Edge]):
    for edge in lst_edges:
        matrix[edge.origin-1][edge.destiny-1] = edge.cost
    return matrix

def floyd(num_vertex: int, num_edges: int, lst_edges: list[Edge]):
    matrix = init_matrix(num_vertex)
    vm = build_value_matrix(matrix, lst_edges)

    for k in range(num_vertex):
        for i in range(num_vertex):
            for j in range(num_vertex):
                if vm[i][k] + vm[k][j] < vm[i][j]:
                    vm[i][j] = vm[i][k] + vm[k][j]
    return vm

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

def main():
    lst_edges = []

    with open("../data/graph1.txt") as f:
        num_vertex, num_edges = [int(x) for x in f.readline().split()]
        for _ in range(num_edges):
            u, v, cost = [int(x) for x in f.readline().split()]
            edge = Edge(u, v, cost)
            lst_edges.append(edge)

    value_matrix = floyd(num_vertex, num_edges, lst_edges)

    central_node, adj_list = find_central_node(value_matrix, num_vertex)

    if central_node is not None:
        print(f"(1) A estação central é: {central_node + 1}")
        print(f"(2) Distâncias da estação central aos demais vértices: {adj_list}")
        print(f"(3) Candidatos a estação central:")
        print("")
        for row in value_matrix:
            print(row)
    else:
        print("Não existe estação central.")

if __name__ == "__main__":
    main()
