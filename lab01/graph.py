"""
Moduł grafowy implementujący:
1. Reprezentację grafów (macierz sąsiedztwa, macierz incydencji, lista sąsiedztwa)
2. Wizualizację grafów
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
        return nx.incidence_matrix(self.G).toarray().astype(int).tolist()
    
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


def generate_gnl_random_graph(n, l):
    if n < 1:
        raise ValueError("Liczba wierzchołków musi być co najmniej 1")
    
    max_edges = n * (n - 1) // 2

    if l > max_edges:
        raise ValueError(f"Za dużo krawędzi. Maksimum to {max_edges} dla {n} wierzchołków")
    
    G = nx.gnm_random_graph(n, l)
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
