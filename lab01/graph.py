"""
Moduł grafowy implementujący:
1. Reprezentację grafów (macierz sąsiedztwa, macierz incydencji, lista sąsiedztwa)
2. Wizualizację grafów (układ kołowy)
3. Generowanie losowych grafów G(n,l) i G(n,p)
"""

import matplotlib.pyplot as plt
import numpy as np
import random
import math


class Graph:
    def __init__(self, vertices, representation_type=None, data=None):
        self.V = vertices
        
        self.adjacency_matrix = [[0] * vertices for _ in range(vertices)]
        self.incidence_matrix = []
        self.adjacency_list = [[] for _ in range(vertices)]
        self.edges = []
        
        if representation_type and data:
            if representation_type == 'adjacency_matrix':
                self.adjacency_matrix = data
                self._from_adjacency_matrix()
            elif representation_type == 'incidence_matrix':
                self.incidence_matrix = data
                self._from_incidence_matrix()
            elif representation_type == 'adjacency_list':
                self.adjacency_list = data
                self._from_adjacency_list()
    
    def add_edge(self, u, v):
        if u >= self.V or v >= self.V or u < 0 or v < 0:
            raise ValueError(f"Indeksy wierzchołków muszą być między 0 a {self.V-1}")
        
        if u == v:
            raise ValueError("Pętle własne nie są dozwolone w grafach prostych")
            
        self.adjacency_matrix[u][v] = 1
        self.adjacency_matrix[v][u] = 1
        
        if v not in self.adjacency_list[u]:
            self.adjacency_list[u].append(v)
        if u not in self.adjacency_list[v]:
            self.adjacency_list[v].append(u)
        
        edge = (min(u, v), max(u, v))
        if edge not in self.edges:
            self.edges.append(edge)
            
        self._update_incidence_matrix()
    
    def _update_incidence_matrix(self):
        self.incidence_matrix = [[0] * len(self.edges) for _ in range(self.V)]
        for edge_idx, (u, v) in enumerate(self.edges):
            self.incidence_matrix[u][edge_idx] = 1
            self.incidence_matrix[v][edge_idx] = 1
    
    def _from_adjacency_matrix(self):
        self.adjacency_list = [[] for _ in range(self.V)]
        self.edges = []
        
        for i in range(self.V):
            for j in range(self.V):
                if self.adjacency_matrix[i][j] == 1:
                    self.adjacency_list[i].append(j)
        
        for i in range(self.V):
            for j in range(i + 1, self.V): 
                if self.adjacency_matrix[i][j] == 1:
                    self.edges.append((i, j))
        
        self._update_incidence_matrix()
    
    def _from_incidence_matrix(self):
        self.adjacency_matrix = [[0] * self.V for _ in range(self.V)]
        self.adjacency_list = [[] for _ in range(self.V)]
        self.edges = []
        
        for edge_idx in range(len(self.incidence_matrix[0])):
            vertices = [v for v in range(self.V) if self.incidence_matrix[v][edge_idx] == 1]
            if len(vertices) == 2:
                u, v = vertices
                self.adjacency_matrix[u][v] = 1
                self.adjacency_matrix[v][u] = 1
                
                if v not in self.adjacency_list[u]:
                    self.adjacency_list[u].append(v)
                if u not in self.adjacency_list[v]:
                    self.adjacency_list[v].append(u)
                  
                self.edges.append((min(u, v), max(u, v)))
    
    def _from_adjacency_list(self):
        self.adjacency_matrix = [[0] * self.V for _ in range(self.V)]
        self.edges = []
        
        for u in range(self.V):
            for v in self.adjacency_list[u]:
                self.adjacency_matrix[u][v] = 1
                if u < v and (u, v) not in self.edges:
                    self.edges.append((u, v))
        
        self._update_incidence_matrix()
    
    def get_adjacency_matrix(self):
        return self.adjacency_matrix
    
    def get_incidence_matrix(self):
        return self.incidence_matrix
    
    def get_adjacency_list(self):
        return self.adjacency_list
    
    def get_edges(self):
        return self.edges
    
    def __str__(self):
        result = f"Graf z {self.V} wierzchołkami i {len(self.edges)} krawędziami\n"
        result += "Macierz sąsiedztwa:\n"
        for row in self.adjacency_matrix:
            result += str(row) + "\n"
        
        result += "\nMacierz incydencji:\n"
        for row in self.incidence_matrix:
            result += str(row) + "\n"
        
        result += "\nLista sąsiedztwa:\n"
        for i, neighbors in enumerate(self.adjacency_list):
            result += f"{i}: {neighbors}\n"
        
        return result


def visualize_circular(graph, title="Graf - Układ kołowy", save_path=None):
    plt.figure(figsize=(10, 10))
    plt.title(title)
    
    num_vertices = graph.V
    
    radius = 5
    angles = np.linspace(0, 2 * np.pi, num_vertices, endpoint=False)
    
    pos = {}
    for i in range(num_vertices):
        pos[i] = (radius * np.cos(angles[i]), radius * np.sin(angles[i]))
    
    for i in range(num_vertices):
        plt.plot(pos[i][0], pos[i][1], 'bo', markersize=20)
        plt.text(pos[i][0], pos[i][1], str(i+1), fontsize=12, 
                 ha='center', va='center', color='white')
    
    for u, v in graph.get_edges():
        plt.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], 'k-', linewidth=1.5)
    
    circle = plt.Circle((0, 0), radius, fill=False, linestyle='dotted', color='red', alpha=0.3)
    plt.gca().add_patch(circle)
    
    plt.axis('equal')
    plt.grid(False)
    plt.axis('off')
    
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
    
    graph = Graph(n)
    
    all_edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    
    selected_edges = random.sample(all_edges, m)
    
    for u, v in selected_edges:
        graph.add_edge(u, v)
    
    return graph


def generate_gnp_random_graph(n, p):
    if n < 1:
        raise ValueError("Liczba wierzchołków musi być co najmniej 1")
    
    if p < 0 or p > 1:
        raise ValueError("Prawdopodobieństwo musi być między 0 a 1")
    
    graph = Graph(n)
    
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                graph.add_edge(i, j)
    
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