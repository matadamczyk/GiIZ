"""
Moduł grafowy implementujący:
1. Reprezentację grafów (macierz sąsiedztwa, macierz incydencji, lista sąsiedztwa)
2. Wizualizację grafów (układ kołowy)
3. Generowanie losowych grafów G(n,l) i G(n,p)
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


class Graph:
    def __init__(self, vertices, representation_type=None, data=None):
        self.V = vertices
        self.G = nx.Graph()
        self.G.add_nodes_from(range(vertices))
        
        if representation_type and data:
            if representation_type == 'adjacency_matrix':
                self._from_adjacency_matrix(data)
            elif representation_type == 'incidence_matrix':
                self._from_incidence_matrix(data)
            elif representation_type == 'adjacency_list':
                self._from_adjacency_list(data)
    
    def add_edge(self, u, v):
        if u >= self.V or v >= self.V or u < 0 or v < 0:
            raise ValueError(f"Indeksy wierzchołków muszą być między 0 a {self.V-1}")
        
        if u == v:
            raise ValueError("Pętle własne nie są dozwolone w grafach prostych")
            
        self.G.add_edge(u, v)
    
    def _from_adjacency_matrix(self, matrix):
        for i in range(self.V):
            for j in range(i + 1, self.V):
                if matrix[i][j] == 1:
                    self.G.add_edge(i, j)
    
    def _from_incidence_matrix(self, matrix):
        for edge_idx in range(len(matrix[0])):
            vertices = [v for v in range(self.V) if matrix[v][edge_idx] == 1]
            if len(vertices) == 2:
                self.G.add_edge(vertices[0], vertices[1])
    
    def _from_adjacency_list(self, adj_list):
        for u in range(self.V):
            for v in adj_list[u]:
                if u < v:
                    self.G.add_edge(u, v)
    
    def get_adjacency_matrix(self):
        return nx.to_numpy_array(self.G).tolist()
    
    def get_incidence_matrix(self):
        return nx.incidence_matrix(self.G).toarray().tolist()
    
    def get_adjacency_list(self):
        return [list(self.G.neighbors(v)) for v in range(self.V)]
    
    def get_edges(self):
        return list(self.G.edges())
    
    def __str__(self):
        result = f"Graf z {self.V} wierzchołkami i {self.G.number_of_edges()} krawędziami\n"
        result += "Macierz sąsiedztwa:\n"
        for row in self.get_adjacency_matrix():
            result += str(row) + "\n"
        
        result += "\nMacierz incydencji:\n"
        for row in self.get_incidence_matrix():
            result += str(row) + "\n"
        
        result += "\nLista sąsiedztwa:\n"
        for i, neighbors in enumerate(self.get_adjacency_list()):
            result += f"{i}: {neighbors}\n"
        
        return result


def visualize_circular(graph, title="Graf - Układ kołowy", save_path=None):
    plt.figure(figsize=(10, 10))
    plt.title(title)
    
    pos = nx.circular_layout(graph.G)
    nx.draw(graph.G, pos, with_labels=True, node_color='lightblue', 
            node_size=500, font_size=12, font_weight='bold')
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()


def generate_gnm_random_graph(n, m):
    if n < 1:
        raise ValueError("Liczba wierzchołków musi być co najmniej 1")
    
    max_edges = n * (n - 1) // 2
    
    if m > max_edges:
        raise ValueError(f"Za dużo krawędzi. Maksimum to {max_edges} dla {n} wierzchołków")
    
    G = nx.gnm_random_graph(n, m)
    graph = Graph(n)
    graph.G = G
    return graph


def generate_gnp_random_graph(n, p):
    if n < 1:
        raise ValueError("Liczba wierzchołków musi być co najmniej 1")
    
    if p < 0 or p > 1:
        raise ValueError("Prawdopodobieństwo musi być między 0 a 1")
    
    G = nx.gnp_random_graph(n, p)
    graph = Graph(n)
    graph.G = G
    return graph


if __name__ == "__main__":
    print("Program do reprezentacji, wizualizacji i generowania losowych grafów")
    print("=" * 70)
    
    print("\n1. Reprezentacja grafów")
    print("-" * 70)
    
    g = Graph(5)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    
    print(g)
    
    adj_matrix = [
        [0, 1, 1, 0, 0],
        [1, 0, 1, 0, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 1, 0, 1],
        [0, 0, 0, 1, 0]
    ]
    g2 = Graph(5, 'adjacency_matrix', adj_matrix)
    print("\nGraf utworzony z macierzy sąsiedztwa:")
    print(g2)
    
    adj_list = [
        [1, 2],
        [0, 2, 3],
        [0, 1, 3],
        [1, 2, 4],
        [3]
    ]
    g3 = Graph(5, 'adjacency_list', adj_list)
    print("\nGraf utworzony z listy sąsiedztwa:")
    print(g3)
    
    print("\n2. Wizualizacja grafów")
    print("-" * 70)
    
    print("Wizualizacja grafu (okno zostanie otwarte)")
    visualize_circular(g, title="Przykładowy Graf - Układ kołowy")
    
    print("\n3. Generowanie losowych grafów")
    print("-" * 70)
    
    n = 7
    m = 10
    g_nm = generate_gnm_random_graph(n, m)
    print(f"Wygenerowany graf G({n},{m}) ma {len(g_nm.get_edges())} krawędzi")
    visualize_circular(g_nm, title=f"Losowy Graf G({n},{m}) - Model G(n,l)")
    
    n = 7
    p = 0.5
    g_np = generate_gnp_random_graph(n, p)
    print(f"Wygenerowany graf G({n},{p}) ma {len(g_np.get_edges())} krawędzi")
    visualize_circular(g_np, title=f"Losowy Graf G({n},{p}) - Model G(n,p)")
    
    print("\nProgram zakończony.") 