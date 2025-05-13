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
    # Konstruktor przyjmujacy liczbe wierzcholkow i opcjonalnie reprezentacje grafu wraz z danymi
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
    
    # Metoda dodajaca krawedzie do grafu
    def add_edge(self, u, v):
        # Sprawdzenie poprawnosci indeksow wierzcholkow
        if u >= self.V or v >= self.V or u < 0 or v < 0:
            raise ValueError(f"Indeksy wierzchołków muszą być między 0 a {self.V-1}")
        
        # Sprawdzenie istnienia petli wlasnych
        if u == v:
            raise ValueError("Pętle własne nie są dozwolone w grafach prostych")
            
        self.G.add_edge(u, v)
    
    # Metoda konwertujaca z macierzy sasiedztwa
    def _from_adjacency_matrix(self, matrix):
        # Przetwarzamy tylko gorny trojkat macierzy poniewaz graf jest nieskierowany
        for i in range(self.V):
            for j in range(i + 1, self.V):
                # Dla kazdej jedynki w macierzy dodajemy odpowiednia krawedz
                if matrix[i][j] == 1:
                    self.G.add_edge(i, j)
    
    # Metoda konwertujaca z macierzy incydencji
    def _from_incidence_matrix(self, matrix):
        # Dla kazdej kolumny macierzy (krawedzi) znajdujemy wierzcholki ktore ja tworza
        for edge_idx in range(len(matrix[0])):
            vertices = [v for v in range(self.V) if matrix[v][edge_idx] == 1]
            # Sprawdzamy czy krawedz laczy dokladnie dwa wierzcholki i dodajemy ją do grafu
            if len(vertices) == 2:
                self.G.add_edge(vertices[0], vertices[1])
    
    # Metoda konwertujaca z listy sasiedztwa
    def _from_adjacency_list(self, adj_list):
        # Dla kazdego wierzcholka przetwarzamy jego liste sasiadow
        for u in range(self.V):
            for v in adj_list[u]:
                # Sprawdzamy czy nie ma duplikatow i dodajemy krawedz
                if u < v:
                    self.G.add_edge(u, v)
    
    # Metoda zwracajaca macierz sasiedztwa
    def get_adjacency_matrix(self):
        return nx.to_numpy_array(self.G).tolist()
    
    # Metoda zwracajaca macierz incydencji
    def get_incidence_matrix(self):
        return nx.incidence_matrix(self.G).toarray().astype(int).tolist()
    
    # Metoda zwracajaca liste sasiedztwa
    def get_adjacency_list(self):
        return [list(self.G.neighbors(v)) for v in range(self.V)]
    
    # Metoda zwracajaca liste krawedzi
    def get_edges(self):
        return list(self.G.edges())
    
    # Metoda zwracajaca reprezentacje grafu w postaci stringa
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


# Metoda wizualizujaca graf
def visualize_circular(graph, title="Graf", save_path=None):
    plt.figure(figsize=(10, 10))
    plt.title(title)
    
    # Ukladamy wierzcholki w okregu
    pos = nx.circular_layout(graph.G)
    nx.draw(graph.G, pos, with_labels=True, node_color='lightblue', 
            node_size=500, font_size=12, font_weight='bold')
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()


# Metoda generujaca graf losowy G(n,l) - n - liczba wierzcholkow, l - liczba krawedzi
def generate_gnm_random_graph(n, l):
    if n < 1:
        raise ValueError("Liczba wierzchołków musi być co najmniej 1")
    
    # Obliczamy maksymalna liczbe krawedzi
    max_edges = n * (n - 1) // 2

    if l > max_edges:
        raise ValueError(f"Za dużo krawędzi. Maksimum to {max_edges} dla {n} wierzchołków")
    
    G = nx.gnm_random_graph(n, l)
    graph = Graph(n)
    graph.G = G
    return graph


# Metoda generujaca graf losowy G(n,p) - n - liczba wierzcholkow, p - prawdopodobienstwo krawedzi
def generate_gnp_random_graph(n, p):
    if n < 1:
        raise ValueError("Liczba wierzchołków musi być co najmniej 1")
    
    if p < 0 or p > 1:
        raise ValueError("Prawdopodobieństwo musi być między 0 a 1")
    
    G = nx.gnp_random_graph(n, p)
    graph = Graph(n)
    graph.G = G
    return graph